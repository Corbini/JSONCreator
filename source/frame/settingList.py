from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar
from source.frame.call import Call
from source.frame.warning import WarningPopUp
from source.frame.setting import Setting
from source.frame.translation import Translation


class ObjectList:
    def __init__(self, parent, value, call_value, get_parent, call_key, number=0):
        self.frame = Frame(parent, padx=10, pady=5)

        self.parent = parent

        self.setting = Setting(parent, self.frame, 'Value', value, call_value)

        self.key = Setting(parent, self.frame, 'Key', '', call_key)

        self._get_parent = get_parent
        self.translation = Translation(self.frame, self.get_parent)

        self.frame.grid(column=((number % 3) + 1), row=(number // 3))

    def get_parent(self, parents: list):
        name_with_catalog = self.setting.get()

        name_with_catalog = name_with_catalog.split('/')

        n = 0
        for names in name_with_catalog:
            parents.insert(n, names)
            n += 1

        self._get_parent(parents)

        print(parents)


class SettingList:
    def __init__(self, parent, parent_frame, name, data="", call=None, translation=False):

        self.frame = Frame(parent_frame)
        self.frame.pack(side='top', anchor='nw')

        self.label = Label(self.frame, text=name)
        self.label.grid(column=0)

        self.parent = parent

        self.name = name
        self.entries = []
        self.number = 0

        self.translation = translation
        call_translation = None
        if self.translation:
            call_translation = self._call_translation

        for value in data:
            if call is not None:
                self.entries.append(ObjectList(self.frame, value, call, self.parent.get_parent,
                                               self._call_key, self.number))
            else:
                self.entries.append(ObjectList(self.frame, value, self._call_value, call_translation, self._call_key,
                                               self.number))
            self.number += 1

    def update_keys(self, keys):
        n = 0
        for key in keys:
            try:
                self.entries[n].key.update(key)
                n += 1
            except IndexError:
                call_translation = None
                if self.translation:
                    call_translation = self._call_translation

                self.entries.append(ObjectList(self.frame, 'value' + str(n), self._call_value, self.parent.get_parent,
                                               self._call_key, self.number))

                n += 1

        return True

    def update(self, data):
        return

        n = 0
        for value in data:
            try:
                self.entries[n].setting.update(value)
            except IndexError:
                translation_call = None
                if self.translation:
                    translation_call = self._call_translation

                self.entries.append(ObjectList(self.frame, value, self._call_value, self.parent.get_parent,
                                               self._call_key, self.number))
                self.number += 1

    def _translations(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

    def _call_value(self, event):

        new_data = []

        for entry in self.entries:
            new_data.append(entry.setting.get())

        new_data = new_data[:-1]

        parents = []
        self.parent.get_parent(parents)

        Call.call(parents, self.name, new_data, 'update')

    def get(self):
        new_data = ''

        for entry in self.entries:
            new_data += entry.setting.get() + ';'

        return new_data[:-1]

    def _call_translation(self, event):
        name_with_catalogs = ''
        value = ''

        for entry in self.entries:
            if entry.translation is event.widget.master:
                name_with_catalogs = entry.setting.get()
                value = entry.translation.get()

        parents = []
        self.parent.get_parent(parents)
        name_with_catalogs = name_with_catalogs.split('/')
        parents = parents + name_with_catalogs[:-1]
        name = name_with_catalogs [-1]

        print(parents[:-1], '\n new_value: ', parents[-1])

        Call.call(parents, name, value, )

        # self.call(parents, name, value, operation)

    def _call_key(self, event):
        key_list = []

        for entry in self.entries:
            key_list.append(entry.key.get())

        parents = []
        self.parent.get_parent(parents)

        Call.call(parents, 'enumKey', key_list, 'update')
