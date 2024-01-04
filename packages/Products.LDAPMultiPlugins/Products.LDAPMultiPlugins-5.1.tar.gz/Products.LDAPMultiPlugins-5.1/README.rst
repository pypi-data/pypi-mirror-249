.. image:: https://github.com/dataflake/Products.LDAPMultiPlugins/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/dataflake/Products.LDAPMultiPlugins/actions/workflows/tests.yml
   :alt: Automated test results

.. image:: https://coveralls.io/repos/github/dataflake/Products.LDAPMultiPlugins/badge.svg
   :target: https://coveralls.io/github/dataflake/Products.LDAPMultiPlugins
   :alt: Test coverage

.. image:: https://readthedocs.org/projects/productsldapmultiplugins/badge/?version=latest
   :target: https://productsldapmultiplugins.readthedocs.io
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/Products.LDAPMultiPlugins.svg
   :target: https://pypi.python.org/pypi/Products.LDAPMultiPlugins
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.LDAPMultiPlugins.svg
   :target: https://pypi.org/project/Products.LDAPMultiPlugins
   :alt: Supported Python versions


===========================
 Products.LDAPMultiPlugins
===========================

The LDAPMultiPlugins package provides `PluggableAuthService
<https://productspluggableauthservice.readthedocs.io>`_ plugins that use
LDAP (standards-conforming implementations as well as ActiveDirectory)
as the backend for the services they provide. The PluggableAuthService
is a Zope user folder product that can be extended in modular fashion using
so-called plugins.

The plugins in this package provide a PluggableAuthService-compatible shim
around a `LDAPUserFolder <https://productsldapuserfolder.readthedocs.io>`_
instance. After instantiating a plugin all further configuration is done on the
LDAPUserFolder object itself, which is created automatically inside the plugin.
Visit the `ZMI` `Configure` tab to find it.
