import tkinter as tk
from tkinter import Canvas, PhotoImage, Text
from source.button import Button


class Main(tk.Frame):

    from ._gui import create_menu, scroll_update , on_scrollwheel

    parameter_tree = None
    from ._tree import tree_update, tree_create, tree_input_set, tree_remove

    def __init__(self, window):
        super().__init__(master=window, bg='#363131')
        self.create_menu()
        self.pack(fill='both', expand=True)

        self.event_add("<<save_as>>", "<Control-S>")
