import tkinter as tk
from tkinter import Canvas, PhotoImage, Text
from source.button import Button


class Main(tk.Frame):

    from ._gui import create_menu, scroll_show, scroll_hide, on_scrollwheel

    parameter_tree = None
    from ._tree import tree_update, tree_create

    def __init__(self, window):
        super().__init__(master=window, width=1000, height=800)
        self.create_menu()
        self.grid()

        self.event_add("<<save_as>>", "<Control-S>")
