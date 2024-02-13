from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry, END
from source.frame.setting import Setting


class Parameter(Frame):

    from ._name import create_name, change_name, configure_name, update_name, show_name_button
    from ._generals import create_generals, show_generals, hide_generals, set_type, entry_input, reset_value, menu_input, remove_parameter

    call = lambda self, parents, name, value, operation: print(parents, name, value, operation)
    languages = lambda self: list()

    def __init__(self, parent, frame, name, type=''):
        super().__init__(
            master=frame
        )
        self.widen = False
        self.pack(side='top', anchor='nw')

        self.par_parent = parent

        self.create_name(name)
        self.languages_gui = dict()
        self.create_generals(type, name)
        
        self.settings_view = Frame(self)
        self.settings_list = dict()

        self.add_button = Button(self.settings_view, text='add', command=self.add_button_event)

    def add_button_event(self):
        parents = list()
        self.get_parent(parents)
        self.call(parents, 'NewParameter', None, 'add')

    def get_parent(self, parents = list()):
        if self.par_parent is not None:
            self.par_parent.get_parent(parents)
            parents.append(self.name_button.cget('text'))
        return parents

    def change_size(self):
        if self.widen is False:

            self.settings_view.grid(row=1, column=1, sticky='nw')
            self.show_generals()

            self.widen = True

        else:
            self.settings_view.grid_forget()
            self.hide_generals()

            self.widen = False

    def update_setting(self, name, value):
        if name == 'name':
            self.par_parent.settings_list.pop(self.name_button.cget('text'))
            self.update_name(value)
            self.par_parent.settings_list[value] = self

        elif name in self.languages_gui.keys():
            self.languages_gui[name][1].delete(0, END)
            self.languages_gui[name][1].insert(0, value)

        elif name == 'valueType':
                self.set_type(value)

        elif name not in self.settings_list:
            self.settings_list[name] = Setting(self, self.settings_view, name, value)
        else:
            self.settings_list[name].update(value)

    def add_child(self, name):
        if name in self.settings_list:
            return

        self.settings_list[name] = Parameter(self, self.settings_view, name)
        self.settings_list[name].update_languages()

    def remove_child(self, child):
        if child in self.settings_list:
            self.settings_list[child].pack_forget()
            self.settings_list[child].destroy()
            self.settings_list.pop(child)

    def update_languages(self):
        parents = []
        self.get_parent(parents)
        for language in self.languages():
            self.call(parents,language, self.name_button.cget('text'), 'get')