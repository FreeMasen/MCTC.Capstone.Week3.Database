'''An interaction with the UI'''
class Interaction():
    '''An interaction with the UI'''
    def __init__(self, value):
        self.initial_value = value
        self.table_names = None
        self.table_name = None
        self.columns = None
        self.add_row = False
        self.row_to_add = list()
        self.remove_row = False
        self.row_id = None
        self.table_to_remove_row_from = None
        self.display_all = False
        self.display_one = False
        self.display_row_id = None
        self.stopped = False
        self.column = None
        self.value = None
        self.table = None
