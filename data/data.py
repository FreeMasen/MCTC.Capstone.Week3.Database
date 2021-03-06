'''Data access layer for SQLite3'''
import sqlite3
from data.column import *
class Data():
    '''A data service'''
    def __init__(self, connection_string='data.db'):
        self.connection_string = connection_string
    def get_table_names(self):
        '''Get a list of all the tables in the database'''
        table_list = self._execute_query('SELECT name FROM sqlite_master WHERE type="table" AND name not like "sqlite%"', 'sqlite_master')
        return list(map(lambda table_tuple: table_tuple[0], table_list.values))
    def create_table(self, name, columns):
        '''Create a database table
        (str, list<Column>) -> void
        '''
        column_defs = list(map(str, columns))
        query = 'CREATE TABLE `{tn}` ({cds})'.format(tn=name, cds=','.join(column_defs))
        self._execute_non_query(query)
    def add_row(self, table_name, values):
        '''Add one row to the named table'''
        values = ','.join(map(self._format_value,values))
        query = 'INSERT INTO {tn} VALUES({vals})'.format(tn=table_name, vals=values)
        self._execute_non_query(query)
    def _format_value(self,value):
        '''formats a value for insertion'''
        if isinstance(value, str):
            return '"%s"' % value
        return '%s' % value
    def update_row(self, table_name, row_id, column_name, new_value):
        '''update one cell in a table'''
        query = 'UPDATE {tn} SET {cn} = {nv} WHERE rowid = {ri}'\
        .format(tn=table_name, ri=row_id, cn=column_name,nv=new_value)
        self._execute_non_query(query)
    def delete_row(self, table_name, row_id):
        '''delete a row from the named table with the id'''
        query = 'DELETE FROM {tn} WHERE rowid = {ri}'.\
        format(tn=table_name, ri=row_id)
        self._execute_non_query(query)
    def get_all(self, table_name):
        '''get all rows from any table'''
        query = 'SELECT rowid, * FROM {tn}'.format(tn=table_name)
        return self._execute_query(query, table_name)
    def get_one(self, table_name, row_id):
        '''gets all columns for one row of
        the named table with the id'''
        query = 'SELECT * FROM {tn} WHERE rowid like {ri} LIMIT 1'.\
        format(tn=table_name, ri=row_id)
        return self._execute_query(query, table_name)
    def _execute_non_query(self, query):
        '''Execute a non-value returning query'''
        connection = sqlite3.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    def _execute_query(self, query, table_name):
        '''Executes a value returning query'''
        connection = sqlite3.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('PRAGMA table_info({tn})'.format(tn=table_name))
        column_types = [DATA_TYPES_DICT[row[2].upper()] for row in cursor.fetchall()]
        return QueryResult(column_names, rows, column_types)
class QueryResult():
    '''The result set from a query'''
    def __init__(self, column_names, values, column_types):
        self.columns = column_names
        #the first column "rowid" will always be an INT
        self.types = [DataType.Integer]
        self.types.extend(column_types)
        self.values = values
