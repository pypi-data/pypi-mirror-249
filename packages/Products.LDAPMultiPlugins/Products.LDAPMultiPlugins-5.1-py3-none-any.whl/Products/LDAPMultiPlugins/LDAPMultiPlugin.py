##############################################################################
#
# Copyright (c) 2005-2023 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" LDAPMultiPlugin, a LDAP-enabled PluggableAuthService plugin
"""

import logging
import os
from urllib.parse import quote_plus

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Acquisition import aq_base
from App.Common import package_home
from App.special_dtml import DTMLFile
from zope.interface import implementedBy

from Products.LDAPUserFolder import manage_addLDAPUserFolder
from Products.PluggableAuthService.interfaces.plugins import \
    IGroupEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import \
    IRoleEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import \
    IUserEnumerationPlugin
from Products.PluggableAuthService.utils import classImplements

from .LDAPPluginBase import LDAPPluginBase


logger = logging.getLogger('event.LDAPMultiPlugin')
_dtmldir = os.path.join(package_home(globals()), 'dtml')
addLDAPMultiPluginForm = DTMLFile('addLDAPMultiPlugin', _dtmldir)


def manage_addLDAPMultiPlugin(self, id, title, REQUEST=None):
    """ Factory method to instantiate a LDAPMultiPlugin """
    # Make sure we really are working in our container (the
    # PluggableAuthService object)
    self = self.this()

    # Instantiate the folderish adapter object
    self._setObject(id, LDAPMultiPlugin(id, title=title))
    lmp = getattr(aq_base(self), id)

    # Put the "real" LDAPUserFolder inside it
    manage_addLDAPUserFolder(lmp)

    # clean out the __allow_groups__ bit because it is not needed here
    # and potentially harmful
    lmp_base = aq_base(lmp)
    if hasattr(lmp_base, '__allow_groups__'):
        del lmp_base.__allow_groups__

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect('%s/manage_main' % self.absolute_url())


class LDAPMultiPlugin(LDAPPluginBase):
    """ The adapter that mediates between the PAS and the LDAPUserFolder """
    security = ClassSecurityInfo()
    meta_type = 'LDAP Multi Plugin'
    zmi_icon = 'fas fa-address-book'

    @security.private
    def getGroupsForPrincipal(self, user, request=None, attr=None):
        """ Fulfill GroupsPlugin requirements """
        view_name = self.getId() + '_getGroupsForPrincipal'
        criteria = {'id': user.getId(), 'attr': attr}

        cached_info = self.ZCacheable_get(view_name=view_name,
                                          keywords=criteria,
                                          default=None)

        if cached_info is not None:
            logger.debug('returning cached results from enumerateUsers')
            return cached_info

        acl = self._getLDAPUserFolder()

        if acl is None:
            return ()

        unmangled_userid = self._demangle(user.getId())
        if unmangled_userid is None:
            return ()

        ldap_user = acl.getUserById(unmangled_userid)

        if ldap_user is None:
            return ()

        groups = acl.getGroups(ldap_user.getUserDN(), attr=attr)

        result = tuple(x[0] for x in groups)
        self.ZCacheable_set(result, view_name=view_name, keywords=criteria)

        return result

    @security.private
    def enumerateUsers(self, id=None, login=None, exact_match=0, sort_by=None,
                       max_results=None, **kw):
        """ Fulfill the UserEnumerationPlugin requirements """
        view_name = self.getId() + '_enumerateUsers'
        criteria = {'id': id, 'login': login, 'exact_match': exact_match,
                    'sort_by': sort_by, 'max_results': max_results}
        criteria.update(kw)

        cached_info = self.ZCacheable_get(view_name=view_name,
                                          keywords=criteria,
                                          default=None)

        if cached_info is not None:
            logger.debug('returning cached results from enumerateUsers')
            return cached_info

        result = []
        acl = self._getLDAPUserFolder()
        login_attr = acl.getProperty('_login_attr')
        uid_attr = acl.getProperty('_uid_attr')
        rdn_attr = acl.getProperty('_rdnattr')
        plugin_id = self.getId()
        edit_url = f'{plugin_id}/{acl.getId()}/manage_userrecords'

        if acl is None:
            return ()

        if exact_match and (id or login):
            if id:
                ldap_user = acl.getUserById(id)
                if ldap_user is not None and ldap_user.getId() != id:
                    ldap_user = None
            elif login:
                ldap_user = acl.getUser(login)
                if ldap_user is not None and ldap_user.getUserName() != login:
                    ldap_user = None

            if ldap_user is not None:
                qs = 'user_dn=%s' % quote_plus(ldap_user.getUserDN())
                result.append({'id': ldap_user.getId(),
                               'login': ldap_user.getProperty(login_attr),
                               'pluginid': plugin_id,
                               'editurl': f'{edit_url}?{qs}'})
        else:
            l_results = []
            seen = []
            ldap_criteria = {}

            if id:
                if uid_attr == 'dn':
                    # Workaround: Due to the way findUser reacts when a DN
                    # is searched for I need to hack around it... This
                    # limits the usefulness of searching by ID if the user
                    # folder uses the full DN aas user ID.
                    ldap_criteria[rdn_attr] = id
                else:
                    ldap_criteria[uid_attr] = id

            if login:
                ldap_criteria[login_attr] = login

            for key, val in kw.items():
                if key not in (login_attr, uid_attr):
                    ldap_criteria[key] = val

            # If no criteria are given create a criteria set that will
            # return all users
            if not login and not id:
                ldap_criteria[login_attr] = ''

            l_results = acl.searchUsers(exact_match=exact_match,
                                        **ldap_criteria)

            for l_res in l_results:

                # If the LDAPUserFolder returns an error, bail
                if l_res.get('sn', '') == 'Error' and \
                   l_res.get('cn', '') == 'n/a':
                    return ()

                if l_res['dn'] not in seen:
                    l_res['id'] = l_res[uid_attr]
                    l_res['login'] = l_res[login_attr]
                    l_res['pluginid'] = plugin_id
                    quoted_dn = quote_plus(l_res['dn'])
                    l_res['editurl'] = f'{edit_url}?user_dn={quoted_dn}'
                    result.append(l_res)
                    seen.append(l_res['dn'])

            if sort_by is not None:
                result.sort(key=lambda item: item.get(sort_by, '').lower())

            if isinstance(max_results, int) and len(result) > max_results:
                result = result[:max_results-1]

        result = tuple(result)
        self.ZCacheable_set(result, view_name=view_name, keywords=criteria)

        return result

    @security.private
    def enumerateGroups(self, id=None, exact_match=False, sort_by=None,
                        max_results=None, **kw):
        """ Fulfill the GroupEnumerationPlugin requirements """
        view_name = self.getId() + '_enumerateGroups'
        criteria = {'id': id, 'exact_match': exact_match,
                    'sort_by': sort_by, 'max_results': max_results}
        criteria.update(kw)

        cached_info = self.ZCacheable_get(view_name=view_name,
                                          keywords=criteria,
                                          default=None)

        if cached_info is not None:
            logger.debug('returning cached results from enumerateGroups')
            return cached_info

        acl = self._getLDAPUserFolder()

        if acl is None:
            return ()

        if (id is not None and not exact_match and not kw):
            # likely from a PAS.getUserById(). In any case 'id' and
            # 'exact_match' means only a single result should be
            # available so try to fetch specific group info from
            # cache.
            group_info = self._getGroupInfoCache(id)
            if group_info is not None:
                return (group_info,)

        if id is None and exact_match:
            raise ValueError('Exact Match requested but no id provided')
        elif id is not None:
            kw[self.groupid_attr] = id

        plugin_id = self.getId()

        results = acl.searchGroups(exact_match=exact_match, **kw)

        if len(results) == 1 and results[0]['cn'] == 'n/a':
            # we didn't give enough known criteria for searches
            return ()

        if isinstance(max_results, int) and len(results) > max_results:
            results = results[:max_results+1]

        for rec in results:
            rec['pluginid'] = plugin_id
            rec['id'] = rec[self.groupid_attr]
            self._setGroupInfoCache(rec)

        results = tuple(results)
        self.ZCacheable_set(results, view_name=view_name, keywords=criteria)

        return results

    @security.private
    def enumerateRoles(self, id=None, exact_match=0, sort_by=None,
                       max_results=None, **kw):
        """ Fulfill the RoleEnumerationPlugin requirements """
        # For LDAP, roles and groups are really one and the same thing.
        # We can simply call enumerateGroups here.
        return self.enumerateGroups(id=id, exact_match=exact_match,
                                    sort_by=sort_by, max_results=max_results,
                                    **kw)


classImplements(LDAPMultiPlugin,
                IUserEnumerationPlugin,
                IGroupsPlugin,
                IGroupEnumerationPlugin,
                IRoleEnumerationPlugin,
                *implementedBy(LDAPPluginBase))

InitializeClass(LDAPMultiPlugin)
