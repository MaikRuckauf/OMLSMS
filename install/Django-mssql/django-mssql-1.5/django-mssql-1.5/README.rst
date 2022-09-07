Django MSSQL Database Backend
=============================

`Django-mssql`_ provies a Django database backend for Microsoft SQL Server.

Documentation is available at `django-mssql.readthedocs.org`_.

Requirements
------------

    * Python 2.7
    * PyWin32_
    * SQL Server Management Studio or Microsoft Data Access Components (MDAC)

SQL Server Versions
-------------------

Supported Versions:
    * 2005
    * 2008
    * 2008r2
    * 2012

The SQL Server version will be detected upon initial connection.

Django Version
--------------

The current version of django-mssql supports Django 1.6. If using an older
version of Django, you will need to use an earlier version of django-mssql.

django-mssql 1.4 supports Django 1.4 and 1.5.


References
----------

    * Django-mssql on PyPi: http://pypi.python.org/pypi/django-mssql
    * DB-API 2.0 specification: http://www.python.org/dev/peps/pep-0249/


.. _`Django-mssql`: https://bitbucket.org/Manfre/django-mssql
.. _django-mssql.readthedocs.org: http://django-mssql.readthedocs.org/
.. _PyWin32: http://sourceforge.net/projects/pywin32/
