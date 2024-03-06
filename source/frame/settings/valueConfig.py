from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar
from source.frame.call import Call


class valueConfig(Frame):

    def _add_enum(self, name, value, option=['True', 'False']):
        frame = Frame(self, height=40, width=300)
        label = Label(frame, text=name)
        variable = StringVar(frame)
        variable.set(value)  # default value

        menu = OptionMenu(frame, variable, "True", "False", command=lambda event: self.input(event, name))
        menu.config(width=15, padx=0, pady=0)
        
        menu.pack(side='left', fill='y', expand=True)
        label.pack(side='left', fill='y', expand=True)
        frame.pack(side='top', anchor='nw')

        self._lines[name] = [frame, label, menu, variable]

    def _add_entry(self, name, value):
        frame = Frame(self, height=40, width=300)
        label = Label(frame, text=name)
        entry = Entry(frame)

        entry.insert(0, value)
        entry.bind('<Return>', lambda event: self.input(event, name))
        entry.bind('<FocusOut>', lambda event: self.reset(event, name))

        entry.pack(side='left', fill='y', expand=True)
        label.pack(side='left', fill='y', expand=True)
        frame.pack(side='top', anchor='nw')

        self._lines[name] = [frame, label, entry]

    def _add_entry_list(self, name, value):
        frame = Frame(self, height=300, width=300)
        label = Label(frame, text=name)
        entry = Entry(frame)

        entry.insert(0, value)
        entry.bind('<Return>', lambda event: self.input(event, name))
        entry.bind('<FocusOut>', lambda event: self.reset(event, name))

        entry.pack(side='left', fill='y', expand=True)
        label.pack(side='left', fill='y', expand=True)
        frame.pack(side='top', anchor='nw')

        self._lines[name] = [frame, label, entry]

    def __init__(self, parent, frame, name, data="", type="None"):
        super().__init__(
            master=frame,
        )

        self.label = Label(self, text=name)
        self.label.pack(side='left', fill='y', expand=True)

        self._lines = dict()

        self._load_type(type)

        self.update(data)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def _load_type(self, type):
        stringables = ['String', 'IP', 'IPv4', 'IPv6', 'SerialPort', 'UserName', 'Password']
        stringables_settings = [
            ["Maximum Bytes", self._add_entry],
            ["Maximum Chars", self._add_entry],
            ["Hidden", self._add_entry]
        ]
        valueable = ['UInt8', 'UInt16', 'UInt32', 'Uint64', 'Int8', 'Int16', 'Int32', 'Int64', 'Real32', 'Real64']
        valueable_settings = [
            ["Minimum", self._add_entry],
            ["Maximum", self._add_entry],
            ["Scaler", self._add_entry],
            ["Is Float", self._add_enum],
            ["Unit", self._add_entry]
        ]

        multi_choice = ['MultiChoice']
        multi_choice_settings = [
            ["View Height", self._add_entry],
            ["Is Ordered", self._add_enum],
            ["Enum List", self._add_entry_list]
        ]

        self._lines = dict()

        if type in stringables:
            for setting in stringables_settings:
                setting[1](setting[0], '')

        elif type in valueable:
            for setting in valueable_settings:
                setting[1](setting[0], '')

        elif type in multi_choice:
            for setting in multi_choice_settings:
                setting[1](setting[0], '')

    def _update_option_menu(self, object, value):
        if isinstance(value, bool):
            if value:
                object.set('True')
            else:
                object.set('False')
        else:
            object.set(value)

    def update(self, data):
        values = data.split('|')

        for value in self._lines:
            if isinstance(self._lines[value][2], OptionMenu):
                self._update_option_menu(self._lines[value][3], values.pop(0))
            elif isinstance(self._lines[value][2], OptionMenu):
                pass
            else:
                self._lines[value][2].delete(0, END)
                self._lines[value][2].insert(0, values.pop(0))

        n = 1 + len(self._lines)
        for overload in values:
            self._add_entry('unknown' + str(n), overload)
            n += 1

        self.old_data = data

    def input(self, event, name):
        if self.par_parent is None:
            return
        
        parents = list()
        self.par_parent.get_parent(parents)

        values = self.old_data.split('|')

        index = list(self._lines).index(name)


        if isinstance(self._lines[name][2], OptionMenu):
                value = self._lines[name][3].get()

                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
        else:
            value = self._lines[name][2].get()

        values[index] = value

        name = self.label.cget("text")

        new_value = ""
        new_value += str(values[0])

        for value in values[1:]:
            new_value += '|'
            new_value += str(value)

        Call.call(parents, name, new_value, 'change')

    def reset(self, event, name):
        values = self.old_data.split('|')
        index = list(self._lines).index(name)

        value = values[index]
    
        self._lines[name][2].delete(0, END)
        self._lines[name][2].insert(0, value)
