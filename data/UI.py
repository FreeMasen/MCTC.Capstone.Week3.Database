'''User interface'''
import os
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
        'Show one ingredient']
        self._display_options(menu_options)
        return Interaction(self._ask_digit('What would you like to do', 6))
    def show_option(self, interaction):
        value = interaction.initial_value
        if value == 0:
            return self.create_database_and_table(interaction)
        if value == 1:
            self._display_options(interaction.table_names)
            table_index = self._ask_digit('Which table would you like to modify', len(interaction.table_names))
            interaction.table_name = interaction.table_names[table_index]
            return interaction
        if value == 2:
            return
        if value == 3:
            return
        if value == 4:
            return
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
                col_type_index = self._ask_digit('What type of data would you like to add?', len(DATA_TYPE_NAMES))
                col_type = DATA_TYPES[col_type_index]
                interaction.columns.append(Column(col_name, col_type))
                if not self._ask_bool('Create another column'): break
        else:
            interaction.stopped = True
        return interaction
    def add_item(self, interaction, table):
        '''add an item to the table named in interaction'''
        self.display_table(interaction.table_name, table)
        for column in table.columns:
            if not column == 'id' or column == 'rowid':
                interaction.row_to_add.append(self._ask_and_confirm('What would you like to add for %s' % column))
        return interaction
    def remove_item(self):
        pass
    def update_item(self):
        pass
    def show_all_items(self):
        pass
    def show_one_item(self):
        pass
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
    def _ask_digit(self, question, max_val):
        while True:
            try:
                val = input(question + '?\n')
                ret = int(val)
                if ret <= max_val:
                    return ret - 1
            except:
                print('I\'m sorry, I didn\'t get that. Please enter a value between 1 and %s' % max_val)
    def _ask_and_confirm(self, question):
        while True:
            response = input(question + '?')
            if self._ask_bool('Are you sure, %s?' % response):
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
