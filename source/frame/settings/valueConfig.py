from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar, Button
from source.frame.call import Call
from source.frame.warning import WarningPopUp
from source.frame.setting import Setting
from source.frame.settingList import SettingList


class EntryList(Frame):
    def __init__(self, parent, name):
        self._main_frame = Frame(parent)
        self._main_frame.pack(side='top')

        self.label = Label(self._main_frame, text=name)
        self.label.pack(side='left', anchor='nw')

        super().__init__(self._main_frame)
        self.pack(side='left', anchor='nw')

        self.add_button = Button(self, text='Add')
        self.add_button.pack(side='bottom')


class valueConfig(Frame):

    template = {}

    def __init__(self, parent, frame, name, data="", config_type="None"):
        super().__init__(
            master=frame,
        )

        self.parent = parent

        self.label = Label(self, text=name)
        self.label.pack(side='left', fill='y', expand=True)

        self._lines = dict()

        self.config_type = config_type
        self._load_type(config_type, data)

        self.update(data)

        self.pack(side='top', anchor='nw')
        self.old_data = data

    def _load_type(self, type, data):

        self._lines = dict()
        data = data.split('|')

        settings = ''

        if type in valueConfig.template['Strings']['types']:
            settings = valueConfig.template['Strings']['settings']

        elif type in valueConfig.template['Values']['types']:
            settings = valueConfig.template['Values']['settings']

        elif type in valueConfig.template['MultiChoices']['types']:
            settings = valueConfig.template['MultiChoices']['settings']
        elif type in valueConfig.template['Tariffs']['types']:
            settings = valueConfig.template['Tariffs']['settings']

        lists = ["Enum List"]

        for setting in settings:
            if len(data) > 0:
                if setting in lists:
                    data_list = data.pop(0)
                    data_list = data_list.split(';')
                    self._lines[setting] = SettingList(self, self, setting, data_list, self._call_value,  True)
                else:
                    self._lines[setting] = Setting(None, self, setting, data.pop(0), self._call_value)
            else:
                if setting in lists:
                    self._lines[setting] = SettingList(self, self, setting, [], self._call_value, True)
                else:
                    self._lines[setting] = Setting(None, self, setting, '', self._call_value)

    def update_keys(self, value) -> bool:
        for setting in self._lines:
            if isinstance(self._lines[setting], SettingList):
                self._lines[setting].update_keys(value)
                return True

        return False

    def update(self, data):
        values = data.split('|')

        for name in self._lines:
            if len(values) != 0:
                my_value = values.pop(0)
            else:
                my_value = ''

            if ';' in my_value:
                my_value = my_value.split(';')

            self._lines[name].update(my_value)

        n = 1 + len(self._lines)
        for overload in values:
            self._lines['unknown' + str(n)] = Setting(None, self, 'Entry', overload, self._call_value)
            n += 1

        self.old_data = data

    def _call_value(self, event):
        data = ''

        for setting in self._lines:
            new_data = self._lines[setting].get()
            if isinstance(new_data, list):
                string_data = ''

                for sub_data in new_data:
                    string_data += sub_data + ';'

                data += string_data[:-1]
            else:
                data += new_data

            data += '|'

        data = data[:-1]

        parents = []
        self.parent.get_parent(parents)

        self.clear_warn()

        Call.call(parents, 'valueConfig', data, 'update')

    def reload_language(self):
        for entry in self._lines:
            if isinstance(self._lines[entry], SettingList):
                self._lines[entry].reload_language()

    def get_parent(self, parent: list):
        return self.parent.get_parent(parent)

    def input(self, event, name):
        if self.parent is None:
            return
        
        parents = list()
        self.parent.get_parent(parents)

        values = self.old_data.split('|')

        index = list(self._lines).index(name)

        if isinstance(self._lines[name][2], OptionMenu):
            value = self._lines[name][3].get()

            if value == 'True':
                value = 1
            if value == 'False':
                value = 0
        else:
            value = self._lines[name][2].get()

        values[index] = value

        name = self.label.cget("text")

        new_value = ""
        new_value += str(values[0])

        for value in values[1:]:
            new_value += '|'
            new_value += str(value)

        Call.call(parents, name, new_value, 'update')

    def update_translation(self, name, value) -> bool:
        for entry in self._lines:
            if isinstance(self._lines[entry], SettingList):
                return self._lines[entry].update_translation(name, value)

    def reset(self, event, name):
        values = self.old_data.split('|')
        index = list(self._lines).index(name)

        value = values[index]
    
        self._lines[name][2].delete(0, END)
        self._lines[name][2].insert(0, value)

    def set_warn(self, text: str):
        text = text.split('|')

        if len(text) == 1 and len(self._lines) != 1:
            print(text[0])
        else:
            for line_text, line in zip(text, self._lines):
                if line_text == '':
                    continue

                self._lines[line].set_warn(line_text)

    def clear_warn(self):
        for line in self._lines:
            self._lines[line].clear_warn()
