'''User interface'''
import os
from pathlib import Path
import monotable.table
from data.interaction import Interaction
from data.column import *
from pyfiglet import Figlet
class UserInterface():
    '''Terminal based user interface'''
    def __init__(self):
        self.banner, self.banner_width = self._construct_banner()
        self.exit = False
    def _construct_banner(self):
        f = Figlet('fender')
        banner_lines = list(filter(lambda line: line.rstrip() != '', f.renderText('Pizza Helper').split('\n')))
        max_width = max(map(len,banner_lines))
        banner_lines.insert(0,'=' * max_width)
        banner_lines.append('To help you manage your pizza ingredients'.center(max_width))
        banner_lines.append('=' * max_width)
        return ('\n'.join(banner_lines), max_width)
    def display_banner(self):
        '''Display the main application banner'''
        self._clear()
        print(self.banner)
    def display_menu(self):
        '''display the menu options'''
        menu_options = ['Create a database and table',\
        'Add an ingredient',\
        'Remove an ingredient',\
        'Update an ingredient',\
        'Show all ingredients',\
        'Show one ingredient',\
        'Quit']
        self._display_options(menu_options)
        return Interaction(self._ask_index('What would you like to do', 7))
    def show_option(self, interaction):
        '''show the first step in the request process'''
        value = interaction.initial_value
        if value == 0: #create table
            return self.create_database_and_table(interaction)
        elif value == 6:
            self.exit = True
            interaction
        else:
            self._display_options(interaction.table_names)
            table_index = self._ask_index('Which table', len(interaction.table_names))
            interaction.table_name = interaction.table_names[table_index]
        return interaction
    def create_database_and_table(self, interaction):
        '''Confirm the creation of databases and tables'''
        print('Currently you have the following tables')
        self._display_options(interaction.table_names)
        if self._ask_bool('Do you want to add another table'):
            interaction.create_table = True
            interaction.table_name = self._ask_and_confirm('What would you like to name your new table')
            interaction.columns = list()
            while True:
                col_name = self._ask_and_confirm('What would you like to name your new column?')
                self._display_options(DATA_TYPE_NAMES)
                col_type_index = self._ask_index('What type of data would you like to add?', len(DATA_TYPE_NAMES))
                col_type = DATA_TYPES[col_type_index]
                interaction.columns.append(Column(col_name, col_type))
                if not self._ask_bool('Create another column'): break
        else:
            interaction.stopped = True
        return interaction
    def add_item(self, interaction, table):
        '''add an item to the table named in interaction'''
        self.display_table(interaction.table_name, table)
        for i, column in enumerate(table.columns):
            if column == 'id' or column == 'rowid':
                continue
            data_type = table.types[i]
            val = None
            if data_type == DataType.Text:
                self._ask_string('What text would you like for %s' % column)
            elif data_type == DataType.Decimal:
                val = self._ask_decimal('What decimal would you like for %s' % column)
            elif data_type == DataType.Integer:
                val = self._ask_int('What whole number would you like for %s' % column)
            elif data_type == DataType.Blob:
                val = self._ask_path('What file would you like to use for %s' % column)
            interaction.row_to_add.append(Column(val, data_type))
        return interaction
    def remove_item(self, interaction):
        self.display_table(interaction.table_name, interaction.table)
        interaction.row_id = self._ask_int('What is the ID of the row you would like to remove')
        return interaction
    def update_item(self, interaction):
        self.display_table(interaction.table_name, interaction.table)
        interaction.row_id = self._ask_int('What is the id of the row you would like to update')
        self._display_options(interaction.table.columns)
        column_index = self._ask_index('Which column would you like to udpate', len(interaction.table.columns))
        column_type = interaction.table.types[column_index]
        interaction.column = interaction.table.columns[column_index]
        question = 'What is the new value'
        if column_type == DataType.Text:
            interaction.value = self._ask_string(question)
        if column_type == DataType.Integer:
            interaction.value = self._ask_int(question)
        if column_type == DataType.Decimal:
            interaction.value = self._ask_decimal(question)
        if column_type == DataType.Blob:
            interaction.value = self._ask_path(question)
        return interaction
    def show_all_items(self, interaction):
        self._display_options(interaction.table_names)
        self._ask_index('Which table would you like to see', len(interaction.table_names))
    def show_one_item(self, Interaction):
        print('%s has %s rows' % (Interaction.table_name, len(Interaction.table.values)))
        Interaction.row_id = self._ask_int('What is the id of row you want to see')
        return Interaction
    def display_table(self, title, query_result):
        '''display the table of data'''
        table_values = query_result.values if len(query_result.values) > 0 else [list('-' * len(query_result.columns))]
        print(monotable.table.table(query_result.columns, cellgrid=table_values,title=title))
    def _display_options(self, options):
        '''Display any list of options in numerical order'''
        for i, option in enumerate(options):
            print('%s. %s'.center(int(self.banner_width / 2) + 8) % (i + 1, option))
    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def _ask_int(self, question, max_val = float('inf')):
        while True:
            try:
                val = input(question + '?\n')
                ret = int(val)
                if ret <= max_val:
                    return ret
                raise ValueError
            except:
                print('I\'m sorry, I didn\'t get that. Please enter a value between 1 and %s' % max_val)
    def _ask_index(self, question, max_val):
        return self._ask_int(question, max_val) - 1
    def _ask_decimal(self, question, max_val = float('inf')):
        while True:
            val = input(question + '?\n')
            try:
                ret = float(val)
                if ret <= max_val:
                    return ret
                raise ValueError
            except:
                print('I didn\'t get that plese enter a valid number')
    def _ask_path(self, question):
        while True:
            val = input(question + '?\n')
            try:
                return open(val).read()
            except:
                print('unfortunatly I was not able to open %s' % val)
    def _ask_string(self, question):
        response = input(question + '?')
    def _ask_and_confirm(self, question):
        while True:
            self._ask_string(question)
            if self._ask_bool('Are you sure, %s' % response):
                return response
    def _ask_bool(self, question):
        while True:
            response = input(question + '?\n')
            if response == '':
                print('I didn\'t get that?')
                continue
            if response[0].lower() == 'y':
                return True
            if response[0].lower() == 'n':
                return False
            print('I didn\'t get that?')
