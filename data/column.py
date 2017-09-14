'''for defining tables in a database'''
from enum import Enum
class Column():
    '''A column definition'''
    def __init__(self, name, data_type, pk=False, auto=False, nullable=True, unique=False, default=None):
        self.name = name
        self.data_type = data_type
        self.primary_key = pk
        self.auto_increment = auto
        self.nullable = nullable
        self.unique = unique
        self.default = default
    def __str__(self):
        ret = '`{cn}` {dt}'.format(cn=self.name, dt=self.data_type.value)
        if self.primary_key:
            ret += ' PRIMARY KEY'
        if self.auto_increment:
            ret += ' AUTOINCREMENT'
        if not self.nullable:
            ret += ' NOT NULL'
        if self.unique:
            ret += ' UNIQUE'
        if self.default is not None:
            ret += ' DEFAULT %s' % self.default
        return ret
    def __repr__(self):
        return self.__str__()
class DataType(Enum):
    '''The available datatypes in sqlite'''
    Text = 'TEXT'
    Integer = 'INTEGER'
    Decimal = 'REAL'
    Blob = 'BLOB'

DATA_TYPE_NAMES = [DataType.Text.value, DataType.Integer.value,\
DataType.Decimal.value, DataType.Blob.value]
DATA_TYPES = [DataType.Text, DataType.Integer, DataType.Decimal, DataType.Blob]
DATA_TYPES_DICT = {'TEXT': DATA_TYPES[0], 'INTEGER': DATA_TYPES[1],\
'REAL': DATA_TYPES[2], 'BLOB': DATA_TYPES[3]}
