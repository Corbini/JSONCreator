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
    def __init__(self,parent, parent_frame, name, data="", call=None, seperator='|', translation=False):

        self.frame = Frame(parent_frame)
        self.frame.pack(side='top', anchor='nw')

        self.label = Label(self.frame, text=name)
        self.label.grid(column=0)

        self.old_values = data
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
            self.entries.append(ObjectList(self.frame, value, self._call_value, call_translation, self.number))
            self.number += 1

        self.call = call

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

    def _call_value(self, parents, name, value, operation):


        if self.parent is None:
            return

        parents = list()
        self.parent.get_parent(parents)

        new_values = list(self.old_values)
        new_values[index] = event.widget.get()

        name = self.label.cget("text")

        Call.call(parents, name, new_values, 'change')

    def _call_translation(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

    def _call_key(self, parents, name, value, operation):
        pass
        # self.call(parents, name, value, operation)

