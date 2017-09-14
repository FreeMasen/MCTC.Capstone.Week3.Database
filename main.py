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
        if interaction.initial_value == 0:
            interaction = u.show_option(interaction)
            if interaction.stopped: continue
            data.create_table(interaction.table_name, interaction.columns)
        elif interaction.initial_value == 1:
            interaction = u.show_option(interaction)
            table = data.get_all(interaction.table_name)
            interaction = u.add_item(interaction, table)
            data.add_row(interaction.table_name, interaction.row_to_add)
        elif interaction.initial_value == 2:
            interaction = u.show_option(interaction)
            table = data.get_all(interaction.table_name)
            u.remove_item()

main()
