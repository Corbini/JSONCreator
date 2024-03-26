from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar
from source.frame.call import Call
from source.frame.warning import WarningPopUp
from source.frame.setting import Setting


class ObjectList:
    def __init__(self, parent, value, call_value, call_translation, number=0):
        self.frame = Frame(parent, padx=10, pady=5)

        self.parent = parent

        self.setting = Setting(parent, self.frame, 'Value', value, call_value)

        if call_translation is not None:
            self.translation = Setting(parent, self.frame, 'Translation', '', call_translation)
        else:
            self.translation = None

        self.key = Setting(parent, self.frame, 'Key', '', call_value)

        self.frame.grid(column=((number % 3) + 1), row=(number // 3))


class SettingList:
    def __init__(self, parent, parent_frame, name, data="", call=None, seperator='|', translation=False):

        self.frame = Frame(parent_frame)
        self.frame.pack(side='top', anchor='nw')

        self.label = Label(self.frame, text=name)
        self.label.grid(column=0)

        self.seperator = seperator
        self.parent = parent

        data = data.split(seperator)

        self.name = name
        self.entries = []
        self.number = 0

        self.translation = translation
        call_translation = None
        if self.translation:
            call_translation = self._call_translation

        for value in data:
            if call is not None:
                self.entries.append(ObjectList(self.frame, value, call, call_translation, self.number))
            else:
                self.entries.append(ObjectList(self.frame, value, self._call_value, call_translation, self.number))
            self.number += 1


    def update_keys(self, keys_list):
        keys = keys_list.split(';')

        n = 0
        for key in keys:
            try:
                self.entries[n].key.update(key)
                n += 1
            except IndexError:
                call_translation = None
                if self.translation:
                    call_translation = self._call_translation

                self.entries.append(ObjectList(self.frame, 'value' + n, self._call_value, call_translation, self.number))

                n += 1

    def update(self, data):
        data = data.split(self.seperator)
        n = 0
        for value in data:
            try:
                self.entries[n].setting.update(value)
            except IndexError:
                translation_call = None
                if self.translation:
                    translation_call = self._call_translation

                self.entries.append(ObjectList(self.frame, value, self._call_value, translation_call, self.number))
                self.number += 1

    def _translations(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

    def _call_value(self, event):

        new_data = ''

        for entry in self.entries:
            new_data += entry.setting.get() + ';'

        new_data = new_data[:-1]

        parents = []
        self.parent.get_parent(parents)

        Call.call(parents, self.name, new_data, 'update')

    def get(self):
        new_data = ''

        for entry in self.entries:
            new_data += entry.setting.get() + ';'

        return new_data[:-1]

    def _call_translation(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

    def _call_key(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

