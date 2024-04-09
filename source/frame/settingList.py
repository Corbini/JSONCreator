from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar, Button, Menu
from source.frame.call import Call
from source.frame.warning import WarningPopUp
from source.frame.setting import Setting
from source.frame.translation import Translation


class ObjectList:

    def __init__(self, parent, value, call_value, get_parent, call_key, number,
                 menu_input=lambda text, object: print(text, str(object))):
        self.frame = Frame(parent, padx=10, pady=5)

        self.parent = parent

        self.setting = Setting(parent, self.frame, 'Value', value, call_value)

        self.key = Setting(parent, self.frame, 'Key', '', call_key)

        self._get_parent = get_parent
        self.translation = Translation(self.frame, self.get_parent)

        self.frame.grid(column=((number % 3) + 1), row=(number // 3))

        #Add Menu
        self.popup = Menu(self.frame, tearoff=0)

        self.menu_input = menu_input

        #Adding Menu Items
        self.popup.add_command(label="Move Up", command=lambda: self.menu_input("move_up", self))
        self.popup.add_command(label="Move Down", command=lambda: self.menu_input("move_down", self))
        self.popup.add_separator()
        self.popup.add_command(label="New before", command=lambda: self.menu_input("add_before", self))
        self.popup.add_command(label="New before", command=lambda: self.menu_input("add_after", self))

        self.setting.data.bind("<Button-3>", self.menu_popup)

    def menu_popup(self, event):
        # display the popup menu
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            #Release the grab
            self.popup.grab_release()

    def get_parent(self, parents: list):
        name_with_catalog = self.setting.get()

        name_with_catalog = name_with_catalog.split('/')

        n = 0
        for names in name_with_catalog:
            parents.insert(n, names)
            n += 1

        self._get_parent(parents)

    def move(self, index):
        self.frame.grid_forget()
        self.frame.grid(column=((index % 3) + 1), row=(index // 3))


class SettingList:
    def __init__(self, parent, parent_frame, name, data="", call=None, translation=False):

        self.frame = Frame(parent_frame)
        self.frame.pack(side='top', anchor='nw')

        self.label = Label(self.frame, text=name)
        self.label.grid(column=0)

        self.parent = parent
        self.par_parent = parent

        self.name = name
        self.entries = []
        self.number = 0

        if call is not None:
            self.callable = call
        else:
            self.callable = self._call_value

        for value in data:
            self._add(value)

        self._addable_button()

    def _add_at(self, index, value='value'):
        if value == 'value':
            value += str(index)

        objectlist = ObjectList(self.frame, value, self.callable, self.parent.get_parent, self._call_key,
                            index, self.menu_update)

        self.entries.insert(index, objectlist)
        self.number += 1

        n = index
        for entry in self.entries[n:]:
            entry.move(n)
            n += 1

    def reload_language(self):
        for entry in self.entries:
            entry.translation.reload_language()

    def _add(self, value='value'):
        if value == 'value':
            value += str(self.number)

        objectlist = ObjectList(self.frame, value, self.callable, self.parent.get_parent, self._call_key,
                            self.number, self.menu_update)

        self.entries.append(objectlist)
        self.number += 1

    def _addable_button(self):
        self.addable = Button(self.frame, text='add', command=self.call_add, padx=10, pady=5)

        self.addable.grid(column=2, row=100)

    def call_add(self):
        self._add()
        self.callable(None)

    def update_keys(self, keys):
        n = 0
        for key in keys:
            try:
                self.entries[n].key.update(key)
                n += 1
            except IndexError:
                self.entries.append(ObjectList(self.frame, 'value' + str(n), self._call_value, self.parent.get_parent,
                                               self._call_key, self.number))

                n += 1

        return True

    def menu_update(self, text, object):
        index = self.entries.index(object)
        match text:
            case 'move_up':
                if index <= 0:
                    return

                entry = self.entries.pop(index)
                self.entries.insert(index - 1, entry)
                entry.move(index - 1)
                self.entries[index].move(index)

                self.callable(None)

            case 'move_down':
                if index >= len(self.entries) - 1:
                    return

                entry = self.entries.pop(index)
                self.entries.insert(index + 1, entry)
                entry.move(index + 1)
                self.entries[index].move(index)

                self.callable(None)
            case 'add_before':
                self._add_at(index)

                self.callable(None)
            case 'add_after':
                self._add_at(index+1)

                self.callable(None)

    def update(self, data):

        n = 0
        for value in data[:len(self.entries)-1]:
            self.entries[n].setting.update(value)
            n += 1

        for value in data[len(self.entries):]:
            self._add(value)

    def _call_value(self, event):

        new_data = []

        for entry in self.entries:
            new_data.append(entry.setting.get())

        new_data = new_data[:-1]
        print(new_data)

        parents = []
        self.parent.get_parent(parents)

        self.clear_warn()

        Call.call(parents, self.name, new_data, 'update')

    def get(self):
        new_data = []

        for entry in self.entries:
            new_data.append(entry.setting.get())

        return new_data

    def _call_key(self, event):
        key_list = []

        for entry in self.entries:
            key_list.append(entry.key.get())

        parents = []
        self.parent.get_parent(parents)

        Call.call(parents, 'enumKey', key_list, 'update')

    def update_translation(self, name, value) -> bool:
        print(name, value)

        parents = value[:-1]


        setting_name = ''

        for parent in parents:
            setting_name += parent + '/'

        setting_name = setting_name[:-1]

        value = value[-1]

        for entry in self.entries:
            if entry.setting.get() == setting_name:
                entry.translation.call_set(name, value)

        return True

    def set_warn(self, text: str):
        text = text.split(';')

        for line_text, entry in zip(text, self.entries):
            if line_text == '':
                continue

            entry.setting.set_warn(line_text)

    def clear_warn(self):
        for entry in self.entries:
            entry.setting.clear_warn()
