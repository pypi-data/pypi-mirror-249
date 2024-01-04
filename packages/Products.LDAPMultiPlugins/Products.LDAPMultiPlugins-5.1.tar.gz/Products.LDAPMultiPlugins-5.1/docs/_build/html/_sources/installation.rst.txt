Installation
============


Prerequisites
-------------
You need to have LDAP libraries and developer files installed prior to
installing :mod:`Products.LDAPMultiPlugins`. The most common implementation
is OpenLDAP.


Install with ``pip``
--------------------

.. code:: 

    $ pip install Products.LDAPMultiPlugins


Install with ``zc.buildout``
----------------------------
Just add :mod:`Products.LDAPMultiPlugins` to the ``eggs`` setting(s) in your
buildout configuration to have it pulled in automatically::

    ...
    eggs =
        Products.LDAPMultiPlugins
    ...
