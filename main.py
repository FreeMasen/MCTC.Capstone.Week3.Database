from data.column import *
from data.data import Data
from data.UI import UserInterface
def main():
    data = Data()
    u = UserInterface()
    u.display_banner()
    while u.exit is not True:
        interaction = u.display_menu()
        interaction.table_names = data.get_table_names()
        interaction = u.show_option(interaction)
        if interaction.initial_value == 0: # add table
            if interaction.stopped:
                continue
            data.create_table(interaction.table_name, interaction.columns)
        elif interaction.initial_value == 1: # add row
            table = data.get_all(interaction.table_name)
            interaction = u.add_item(interaction, table)
            data.add_row(interaction.table_name, interaction.row_to_add)
        elif interaction.initial_value == 2: # remove row
            interaction.table = data.get_all(interaction.table_name)
            interaction = u.remove_item(interaction)
            data.delete_row(interaction.table_name, interaction.row_id)
        elif interaction.initial_value == 3: # update row
            interaction.table = data.get_all(interaction.table_name)
            print('table types', interaction.table.types)
            interaction = u.update_item(interaction)
            data.update_row(interaction.table_name, interaction.row_id,interaction.column,interaction.value)
        elif interaction.initial_value == 4: # show all rows
            interaction.table = data.get_all(interaction.table_name)
            u.display_table(interaction.table_name, interaction.table)
        elif interaction.initial_value == 5: # show one row
            interaction.table = data.get_all(interaction.table_name)
            interaction = u.show_one_item(interaction)
            interaction.table = data.get_one(interaction.table_name, interaction.row_id)
            u.display_table(interaction.table_name, interaction.table)
    print('Good bye')
main()
