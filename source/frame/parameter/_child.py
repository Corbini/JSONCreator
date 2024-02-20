from tkinter import Frame, Button
from source.frame.call import Call


class Child(Frame):
    def __init__(self, frame, parents = lambda empty_list: list(empty_list)):
        super().__init__(frame)
        
        self.list = dict()
        self.parents = parents

        self.addable = Button(self, text='add', command=self.call_add)

    def show_addable(self):
        self.addable.pack(side='bottom', anchor='nw')

    def hide_addable(self):
        self.addable.pack_forget()

    def call_add(self):
        parents = list()
        self.parents(parents)
        Call.call(parents, 'NewParameter', None, 'add')

    def show(self):
        self.grid(row=1, column=1, sticky='nw')

    def hide(self):
        self.grid_forget()
        
    def remove(self, name):
        if name in self.list:
            self.list[name].pack_forget()
            self.list[name].destroy()
            self.list.pop(name)

    def rename(self, old_name, new_name):
        self.list[new_name] = self.list.pop(old_name)