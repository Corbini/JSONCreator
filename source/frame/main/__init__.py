import tkinter as tk


class Main(tk.Frame):

    from ._gui import create_menu

    parameter_tree = None
    from ._tree import tree_update, tree_create, tree_remove, tree_reload_list, tree_data_error

    def __init__(self, window):
        super().__init__(master=window, bg='#363131')
        self.create_menu()
        self.pack(fill='both', expand=True)

        self.event_add("<<save_as>>", "<Control-S>")
