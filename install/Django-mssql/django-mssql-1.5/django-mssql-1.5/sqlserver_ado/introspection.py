from __future__ import absolute_import, unicode_literals

from django.db.backends import BaseDatabaseIntrospection
from . import ado_consts

try:
    # Added with Django 1.7
    from django.db.backends import FileInfo
except ImportError:
    from collections import namedtuple
    # Structure returned by the DB-API cursor.description interface (PEP 249)
    FieldInfo = namedtuple('FieldInfo',
        'name type_code display_size internal_size precision scale null_ok')

AUTO_FIELD_MARKER = -1000
BIG_AUTO_FIELD_MARKER = -1001
MONEY_FIELD_MARKER = -1002

class DatabaseIntrospection(BaseDatabaseIntrospection):
    def get_table_list(self, cursor):
        "Return a list of table and view names in the current database."
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' UNION SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS")
        return [row[0] for row in cursor.fetchall()]

    def _is_auto_field(self, cursor, table_name, column_name):
        """Check if a column is an identity column.

        See: http://msdn2.microsoft.com/en-us/library/ms174968.aspx
        """
        sql = "SELECT COLUMNPROPERTY(OBJECT_ID(N'%s'), N'%s', 'IsIdentity')" % \
            (table_name, column_name)

        cursor.execute(sql)
        return cursor.fetchone()[0]

    def _get_table_field_type_map(self, cursor, table_name):
        """
        Return a dict mapping field name to data type. DB-API cursor description 
        interprets the date columns as chars.
        """
        cursor.execute('''
SELECT [COLUMN_NAME], [DATA_TYPE], [CHARACTER_MAXIMUM_LENGTH]
FROM INFORMATION_SCHEMA.COLUMNS
WHERE [TABLE_NAME] LIKE \'%s\'
        ''' % table_name)
        results = dict([(c[0], (c[1], c[2])) for c in cursor.fetchall()])
        return results

    def _datatype_to_ado_type(self, datatype):
        """
        Map datatype name to ado type.
        """
        return {
            'bigint': ado_consts.adBigInt,
            'binary': ado_consts.adBinary,
            'bit': ado_consts.adBoolean,
            'char': ado_consts.adChar,
            'date': ado_consts.adDBDate,
            'datetime': ado_consts.adDBTimeStamp,
            'datetime2': ado_consts.adDBTimeStamp,
            'datetimeoffset': ado_consts.adDBTimeStamp,
            'decimal': ado_consts.adDecimal,
            'float': ado_consts.adDouble,
            'image': ado_consts.adVarBinary,
            'int': ado_consts.adInteger,
            'money': MONEY_FIELD_MARKER,
            'numeric': ado_consts.adNumeric,
            'nchar': ado_consts.adWChar,
            'ntext': ado_consts.adLongVarWChar,
            'nvarchar': ado_consts.adVarWChar,
            'smalldatetime': ado_consts.adDBTimeStamp,
            'smallint': ado_consts.adSmallInt,
            'smallmoney': MONEY_FIELD_MARKER,
            'text': ado_consts.adLongVarChar,
            'time': ado_consts.adDBTime,
            'tinyint': ado_consts.adTinyInt,
            'varbinary': ado_consts.adVarBinary,
            'varchar': ado_consts.adVarChar,
        }.get(datatype.lower(), None)

    def get_table_description(self, cursor, table_name, identity_check=True):
        """Return a description of the table, with DB-API cursor.description interface.

        The 'auto_check' parameter has been added to the function argspec.
        If set to True, the function will check each of the table's fields for the
        IDENTITY property (the IDENTITY property is the MSSQL equivalent to an AutoField).

        When a field is found with an IDENTITY property, it is given a custom field number
        of SQL_AUTOFIELD, which maps to the 'AutoField' value in the DATA_TYPES_REVERSE dict.
        """
        table_field_type_map = self._get_table_field_type_map(cursor, table_name)

        cursor.execute("SELECT * FROM [%s] where 1=0" % (table_name))
        columns = cursor.description

        items = list()
        for column in columns:
            column = list(column) # Convert tuple to list
            # fix data type
            data_type, char_length = table_field_type_map.get(column[0])
            column[1] = self._datatype_to_ado_type(data_type)

            if identity_check and self._is_auto_field(cursor, table_name, column[0]):
                if column[1] == ado_consts.adBigInt:
                    column[1] = BIG_AUTO_FIELD_MARKER
                else:
                    column[1] = AUTO_FIELD_MARKER

            if column[1] == MONEY_FIELD_MARKER:
                # force decimal_places=4 to match data type. Cursor description thinks this column is a string
                column[5] = 4
            elif column[1] == ado_consts.adVarWChar and char_length == -1:
                # treat varchar(max) as text
                column[1] = self._datatype_to_ado_type('text')
            items.append(FieldInfo(*column))
        return items

    def _name_to_index(self, cursor, table_name):
        """Return a dictionary of {field_name: field_index} for the given table.
        
        Indexes are 0-based.
        """
        return dict([(d[0], i) for i, d in enumerate(self.get_table_description(cursor, table_name, False))])

    def get_relations(self, cursor, table_name):
        source_field_dict = self._name_to_index(cursor, table_name)

        sql = """
select
    COLUMN_NAME = fk_cols.COLUMN_NAME,
    REFERENCED_TABLE_NAME = pk.TABLE_NAME,
    REFERENCED_COLUMN_NAME = pk_cols.COLUMN_NAME
from INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS ref_const
join INFORMATION_SCHEMA.TABLE_CONSTRAINTS fk
	on ref_const.CONSTRAINT_CATALOG = fk.CONSTRAINT_CATALOG
	and ref_const.CONSTRAINT_SCHEMA = fk.CONSTRAINT_SCHEMA
	and ref_const.CONSTRAINT_NAME = fk.CONSTRAINT_NAME
	and fk.CONSTRAINT_TYPE = 'FOREIGN KEY'

join INFORMATION_SCHEMA.TABLE_CONSTRAINTS pk
	on ref_const.UNIQUE_CONSTRAINT_CATALOG = pk.CONSTRAINT_CATALOG
	and ref_const.UNIQUE_CONSTRAINT_SCHEMA = pk.CONSTRAINT_SCHEMA
	and ref_const.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME
	And pk.CONSTRAINT_TYPE = 'PRIMARY KEY'

join INFORMATION_SCHEMA.KEY_COLUMN_USAGE fk_cols
	on ref_const.CONSTRAINT_NAME = fk_cols.CONSTRAINT_NAME

join INFORMATION_SCHEMA.KEY_COLUMN_USAGE pk_cols
	on pk.CONSTRAINT_NAME = pk_cols.CONSTRAINT_NAME
where
	fk.TABLE_NAME = %s"""

        cursor.execute(sql,[table_name])
        relations = cursor.fetchall()
        relation_map = dict()

        for source_column, target_table, target_column in relations:
            target_field_dict = self._name_to_index(cursor, target_table)
            target_index = target_field_dict[target_column]
            source_index = source_field_dict[source_column]

            relation_map[source_index] = (target_index, target_table)

        return relation_map

    def get_key_columns(self, cursor, table_name):
        """
        Backends can override this to return a list of (column_name, referenced_table_name,
        referenced_column_name) for all key columns in given table.
        """
        source_field_dict = self._name_to_index(cursor, table_name)

        sql = """
select
    COLUMN_NAME = fk_cols.COLUMN_NAME,
    REFERENCED_TABLE_NAME = pk.TABLE_NAME,
    REFERENCED_COLUMN_NAME = pk_cols.COLUMN_NAME
from INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS ref_const
join INFORMATION_SCHEMA.TABLE_CONSTRAINTS fk
    on ref_const.CONSTRAINT_CATALOG = fk.CONSTRAINT_CATALOG
    and ref_const.CONSTRAINT_SCHEMA = fk.CONSTRAINT_SCHEMA
    and ref_const.CONSTRAINT_NAME = fk.CONSTRAINT_NAME
    and fk.CONSTRAINT_TYPE = 'FOREIGN KEY'

join INFORMATION_SCHEMA.TABLE_CONSTRAINTS pk
    on ref_const.UNIQUE_CONSTRAINT_CATALOG = pk.CONSTRAINT_CATALOG
    and ref_const.UNIQUE_CONSTRAINT_SCHEMA = pk.CONSTRAINT_SCHEMA
    and ref_const.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME
    And pk.CONSTRAINT_TYPE = 'PRIMARY KEY'

join INFORMATION_SCHEMA.KEY_COLUMN_USAGE fk_cols
    on ref_const.CONSTRAINT_NAME = fk_cols.CONSTRAINT_NAME

join INFORMATION_SCHEMA.KEY_COLUMN_USAGE pk_cols
    on pk.CONSTRAINT_NAME = pk_cols.CONSTRAINT_NAME
where
    fk.TABLE_NAME = %s"""

        cursor.execute(sql,[table_name])
        relations = cursor.fetchall()

        key_columns = []
        key_columns.extend([(source_column, target_table, target_column) \
            for source_column, target_table, target_column in relations])
        return key_columns

    def get_indexes(self, cursor, table_name):
    #    Returns a dictionary of fieldname -> infodict for the given table,
    #    where each infodict is in the format:
    #        {'primary_key': boolean representing whether it's the primary key,
    #         'unique': boolean representing whether it's a unique index}
        sql = """
select
	C.name as [column_name],
	IX.is_unique as [unique],
    IX.is_primary_key as [primary_key]
from
	sys.tables T
	join sys.index_columns IC on IC.object_id = T.object_id
	join sys.columns C on C.object_id = T.object_id and C.column_id = IC.column_id
	join sys.indexes IX on IX.object_id = T.object_id and IX.index_id = IC.index_id
where
	T.name = %s
    -- Omit multi-column keys
	and not exists (
		select *
		from sys.index_columns cols
		where
			cols.object_id = T.object_id
			and cols.index_id = IC.index_id
			and cols.key_ordinal > 1
	)
"""
        cursor.execute(sql,[table_name])
        constraints = cursor.fetchall()
        indexes = dict()

        for column_name, unique, primary_key in constraints:
            indexes[column_name.lower()] = {"primary_key":primary_key, "unique":unique}

        return indexes


    data_types_reverse = {
        AUTO_FIELD_MARKER: 'AutoField',
        BIG_AUTO_FIELD_MARKER: 'sqlserver_ado.fields.BigAutoField',
        MONEY_FIELD_MARKER: 'DecimalField',
        ado_consts.adBoolean: 'BooleanField',
        ado_consts.adChar: 'CharField',
        ado_consts.adWChar: 'CharField',
        ado_consts.adDecimal: 'DecimalField',
        ado_consts.adNumeric: 'DecimalField',
        ado_consts.adDate: 'DateField',
        ado_consts.adDBDate: 'DateField',
        ado_consts.adDBTime: 'TimeField',
        ado_consts.adDBTimeStamp: 'DateTimeField',
        ado_consts.adDouble: 'FloatField',
        ado_consts.adSingle: 'FloatField',
        ado_consts.adInteger: 'IntegerField',
        ado_consts.adBigInt: 'BigIntegerField',
        ado_consts.adSmallInt: 'SmallIntegerField',
        ado_consts.adTinyInt: 'SmallIntegerField',
        ado_consts.adVarChar: 'CharField',
        ado_consts.adVarWChar: 'CharField',
        ado_consts.adLongVarWChar: 'TextField',
        ado_consts.adLongVarChar: 'TextField',
        ado_consts.adBinary: 'BinaryField',
        ado_consts.adVarBinary: 'BinaryField',
    }

    def get_constraints(self, cursor, table_name):
        """
        Retrieves any constraints or keys (unique, pk, fk, check, index)
        across one or more columns.

        Returns a dict mapping constraint names to their attributes,
        where attributes is a dict with keys:
         * columns: List of columns this covers
         * primary_key: True if primary key, False otherwise
         * unique: True if this is a unique constraint, False otherwise
         * foreign_key: (table, column) of target, or None
         * check: True if check constraint, False otherwise
         * index: True if index, False otherwise.

        Some backends may return special constraint names that don't exist
        if they don't name constraints of a certain type (e.g. SQLite)
        """
        constraints = dict()

        # getting indexes (primary keys, unique, regular)
        sql = """
        select object_id, name, index_id, is_unique, is_primary_key
        from sys.indexes where object_id = OBJECT_ID(%s)
        """
        cursor.execute(sql,[table_name])
        for object_id, name, index_id, unique, primary_key in list(cursor.fetchall()):
            sql = """
            select name from sys.index_columns ic
            inner join sys.columns c on ic.column_id = c.column_id and ic.object_id = c.object_id
            where ic.object_id = %s and ic.index_id = %s
            """
            cursor.execute(sql, [object_id, index_id])
            columns = [row[0] for row in cursor.fetchall()]
            constraint = {"columns": list(columns),
                          "primary_key": primary_key,
                          "unique": unique,
                          "index": True,
                          "check": False,
                          "foreign_key": None,
                          }
            constraints[name] = constraint

        # getting foreign keys
        sql = """
        select fk.object_id, fk.name, rt.name from sys.foreign_keys fk
        inner join sys.tables rt on fk.referenced_object_id = rt.object_id
        where fk.parent_object_id = OBJECT_ID(%s)
        """
        cursor.execute(sql, [table_name])
        for id, name, ref_table_name in list(cursor.fetchall()):
            sql = """
            select cc.name, rc.name from sys.foreign_key_columns fkc
            inner join sys.columns rc on fkc.referenced_object_id = rc.object_id and fkc.referenced_column_id = rc.column_id
            inner join sys.columns cc on fkc.parent_object_id = cc.object_id and fkc.parent_column_id = cc.column_id
            where fkc.constraint_object_id = %s
            """
            cursor.execute(sql, [id])
            columns, fkcolumns = zip(*cursor.fetchall())
            constraint = {"columns": list(columns),
                          "primary_key": False,
                          "unique": False,
                          "index": False,
                          "check": False,
                          "foreign_key": (ref_table_name, fkcolumns[0]),
                          }
            constraints[name] = constraint

        # get check constraints
        sql = """
        SELECT kc.constraint_name, kc.column_name
        FROM information_schema.constraint_column_usage AS kc
        JOIN information_schema.table_constraints AS c ON
            kc.table_schema = c.table_schema AND
            kc.table_name = c.table_name AND
            kc.constraint_name = c.constraint_name
        WHERE
            c.constraint_type = 'CHECK' 
            AND
            kc.table_name = %s
        """
        cursor.execute(sql,[table_name])
        for constraint, column in list(cursor.fetchall()):
            if column not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "primary_key": False,
                    "unique": False,
                    "index": False,
                    "check": True,
                    "foreign_key": None,
                }
            constraints[constraint]['columns'].append(column)

        return constraints
