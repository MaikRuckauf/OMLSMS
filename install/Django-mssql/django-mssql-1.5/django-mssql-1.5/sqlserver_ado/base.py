"""Microsoft SQL Server database backend for Django."""
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.backends import BaseDatabaseWrapper, BaseDatabaseFeatures, BaseDatabaseValidation, BaseDatabaseClient
from django.db.backends.signals import connection_created
from django.db.utils import InterfaceError
from django.utils.functional import cached_property
from django.utils import six

from . import dbapi as Database

from .introspection import DatabaseIntrospection
from .creation import DatabaseCreation
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor

try:
    import pytz
except ImportError:
    pytz = None

IntegrityError = Database.IntegrityError

class DatabaseFeatures(BaseDatabaseFeatures):
    uses_custom_query_class = True
    has_bulk_insert = False
    
    # DateTimeField doesn't support timezones, only DateTimeOffsetField
    supports_timezones = False
    supports_sequence_reset = False
    
    can_return_id_from_insert = True
    
    supports_regex_backreferencing = False
    
    supports_tablespaces = True
    
    ignores_nulls_in_unique_constraints = False

    can_introspect_autofield = True

    supports_subqueries_in_group_by = False

    allow_sliced_subqueries = False

    uses_savepoints = True

    supports_paramstyle_pyformat = False

    closed_cursor_error_class = InterfaceError

    # connection_persists_old_columns = True

    @cached_property
    def has_zoneinfo_database(self):
        return pytz is not None

def is_ip_address(value):
    """
    Returns True if value is a valid IP address, otherwise False.
    """
    # IPv6 added with Django 1.4
    from django.core.validators import validate_ipv46_address as ip_validator

    try:
        ip_validator(value)
    except ValidationError:
        return False
    return True

def connection_string_from_settings():
    from django.conf import settings
    db_settings = getattr(settings, 'DATABASES', {}).get('default', None)
    return make_connection_string(db_settings)

def make_connection_string(settings):
    db_name = settings['NAME'].strip()
    db_host = settings['HOST'] or '127.0.0.1'
    db_port = settings['PORT']
    db_user = settings['USER']
    db_password = settings['PASSWORD']
    options = settings.get('OPTIONS', {})

    if len(db_name) == 0:
        raise ImproperlyConfigured("You need to specify a DATABASE NAME in your Django settings file.")

    # Connection strings courtesy of:
    # http://www.connectionstrings.com/?carrier=sqlserver

    # If a port is given, force a TCP/IP connection. The host should be an IP address in this case.
    if db_port:
        if not is_ip_address(db_host):
            raise ImproperlyConfigured("When using DATABASE PORT, DATABASE HOST must be an IP address.")
        try:
            port = int(db_port)
        except ValueError:
            raise ImproperlyConfigured("DATABASE PORT must be a number.")
        db_host = '{0},{1};Network Library=DBMSSOCN'.format(db_host, db_port)

    # If no user is specified, use integrated security.
    if db_user != '':
        auth_string = 'UID={0};PWD={1}'.format(db_user, db_password)
    else:
        auth_string = 'Integrated Security=SSPI'

    parts = [
        'DATA SOURCE={0};Initial Catalog={1}'.format(db_host, db_name),
        auth_string
    ]

    if not options.get('provider', None):
        options['provider'] = 'sqlncli10'
    
    parts.append('PROVIDER={0}'.format(options['provider']))

    if 'sqlncli' in options['provider'].lower():
        # native client needs a compatibility mode that behaves like OLEDB
        parts.append('DataTypeCompatibility=80')

    if options.get('use_mars', True):
        parts.append('MARS Connection=True')
    
    if options.get('extra_params', None):
        parts.append(options['extra_params'])    
    
    return ";".join(parts)


VERSION_SQL2000 = 8
VERSION_SQL2005 = 9
VERSION_SQL2008 = 10
VERSION_SQL2012 = 11

class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'microsoft'

    Database = Database

    operators = {
        "exact": "= %s",
        "iexact": "LIKE %s ESCAPE '\\'",
        "contains": "LIKE %s ESCAPE '\\'",
        "icontains": "LIKE %s ESCAPE '\\'",
        "gt": "> %s",
        "gte": ">= %s",
        "lt": "< %s",
        "lte": "<= %s",
        "startswith": "LIKE %s ESCAPE '\\'",
        "endswith": "LIKE %s ESCAPE '\\'",
        "istartswith": "LIKE %s ESCAPE '\\'",
        "iendswith": "LIKE %s ESCAPE '\\'",
    }

    def __init__(self, *args, **kwargs):
        self.use_transactions = kwargs.pop('use_transactions', None)
        
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        try:
            self.command_timeout = int(self.settings_dict.get('COMMAND_TIMEOUT', 30))
        except ValueError:   
            self.command_timeout = 30
        
        options = self.settings_dict.get('OPTIONS', {})
        try:
            self.cast_avg_to_float = not bool(options.get('disable_avg_cast', False))
        except ValueError:
            self.cast_avg_to_float = False

        USE_LEGACY_DATE_FIELDS_DEFAULT = True
        try:
            self.use_legacy_date_fields = bool(options.get('use_legacy_date_fields', USE_LEGACY_DATE_FIELDS_DEFAULT))
        except ValueError:
            self.use_legacy_date_fields = USE_LEGACY_DATE_FIELDS_DEFAULT

        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = BaseDatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = BaseDatabaseValidation(self)

    def get_new_connection(self, conn_params):
        """Connect to the database"""
        conn = self._get_new_connection(conn_params)
        # The OUTPUT clause is supported in 2005+ sql servers
        self.features.can_return_id_from_insert = self._is_sql2005_and_up(conn)
        self.features.has_bulk_insert = self._is_sql2008_and_up(conn)
        if self.settings_dict["OPTIONS"].get("allow_nulls_in_unique_constraints", True):
            self.features.ignores_nulls_in_unique_constraints = self._is_sql2008_and_up(conn)
            if self._is_sql2008_and_up(conn):
                self.creation.sql_create_model = self.creation.sql_create_model_sql2008
        return conn

    def get_connection_params(self):
        """Returns a dict of parameters suitable for get_new_connection."""
        settings_dict = self.settings_dict.copy()
        if settings_dict['NAME'] == '':
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value.")
        if not settings_dict['NAME']:
            # if _nodb_connection, connect to master
            settings_dict['NAME'] = 'master'

        autocommit = settings_dict.get('OPTIONS', {}).get('autocommit', False)
        return {
            'connection_string': make_connection_string(settings_dict),
            'timeout': self.command_timeout,
            'use_transactions': not autocommit,
            }

    def get_new_connection(self, conn_params):
        """Opens a connection to the database."""
        self.__connection_string = conn_params.get('connection_string', '')
        conn = Database.connect(**conn_params)
        return conn

    def init_connection_state(self):
        """Initializes the database connection settings."""
        # if 'mars connection=true' in self.__connection_string.lower():
        #     # Issue #41 - Cannot use MARS with savepoints
        #     self.features.uses_savepoints = False
        # cache the properties on the connection
        self.connection.adoConnProperties = dict([(x.Name, x.Value) for x in self.connection.adoConn.Properties])

        if self.is_sql2000(make_connection=False):
            # SQL 2000 doesn't support the OUTPUT clause
            self.features.can_return_id_from_insert = False

    def create_cursor(self):
        """Creates a cursor. Assumes that a connection is established."""
        cursor = self.connection.cursor()
        return cursor

    def _set_autocommit(self, value):
        self.connection.set_autocommit(value)

    def __get_dbms_version(self, make_connection=True):
        """
        Returns the 'DBMS Version' string, or ''. If a connection to the database has not already
        been established, a connection will be made when `make_connection` is True.
        """
        if not self.connection and make_connection:
            self.connect()
        return self.connection.adoConnProperties.get('DBMS Version', '') if self.connection else ''

    def is_sql2000(self, make_connection=True):
        """
        Returns True if the current connection is SQL2000. Establishes a
        connection if needed when make_connection is True.
        """
        return self.__get_dbms_version(make_connection).startswith(unicode(VERSION_SQL2000))

    def is_sql2005(self, make_connection=True):
        """
        Returns True if the current connection is SQL2005. Establishes a
        connection if needed when make_connection is True.
        """
        return self.__get_dbms_version(make_connection).startswith(unicode(VERSION_SQL2005))

    def is_sql2008(self, make_connection=True):
        """
        Returns True if the current connection is SQL2008. Establishes a
        connection if needed when make_connection is True.
        """
        return self.__get_dbms_version(make_connection).startswith(unicode(VERSION_SQL2008))

    def disable_constraint_checking(self):
        """
        Turn off constraint checking for every table
        """
        if self.connection:
            cursor = self.connection.cursor()
        else:
            cursor = self._cursor()
        cursor.execute('EXEC sp_MSforeachtable "ALTER TABLE ? NOCHECK CONSTRAINT all"')
        return True

    def enable_constraint_checking(self):
        """
        Turn on constraint checking for every table
        """
        if self.connection:
            cursor = self.connection.cursor()
        else:
            cursor = self._cursor()
        # don't check the data, just turn them on
        cursor.execute('EXEC sp_MSforeachtable "ALTER TABLE ? WITH NOCHECK CHECK CONSTRAINT all"')

    def check_constraints(self, table_names=None):
        """
        Check the table constraints.
        """
        if self.connection:
            cursor = self.connection.cursor()
        else:
            cursor = self._cursor()
        if not table_names:
            result = cursor.execute('DBCC CHECKCONSTRAINTS WITH ALL_CONSTRAINTS')
            if cursor.description:
                raise self.Database.IntegrityError(cursor.fetchall())
        else:
            qn = self.ops.quote_name
            for name in table_names:
                cursor.execute('DBCC CHECKCONSTRAINTS({0}) WITH ALL_CONSTRAINTS'.format(
                    qn(name)
                ))
                if cursor.description:
                    raise self.Database.IntegrityError(cursor.fetchall())

    # # MS SQL Server doesn't support explicit savepoint commits; savepoints are
    # # implicitly committed with the transaction.
    # # Ignore them.
    def _savepoint_commit(self, sid):
        # if something is populating self.queries, include a fake entry to avoid
        # issues with tests that use assertNumQueries.
        if self.queries:
            self.queries.append({
                'sql': '-- RELEASE SAVEPOINT %s -- (because assertNumQueries)' % self.ops.quote_name(sid),
                'time': '0.000',
            })

    def is_usable(self):
        try:
            # Use a mssql cursor directly, bypassing Django's utilities.
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Database.DatabaseError:
            return False
        else:
            return True

    def schema_editor(self, *args, **kwargs):
        return DatabaseSchemaEditor(self, *args, **kwargs)
