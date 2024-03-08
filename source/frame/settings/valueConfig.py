from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar, Button
from source.frame.call import Call


class EnumEntry(Entry):

    remove = lambda data: print('Remove: ', data)

    def __init__(self, parent, data):
        self._main_frame = Frame(parent)
        self._main_frame.pack(side='top')

        super().__init__(self._main_frame)
        self.insert(0, data)
        self.pack(side='left')

        self.remove_button = Button(self._main_frame, text='remove', command=self._remove)
        self.remove_button.pack(side='right')

    def _remove(self):
        EnumEntry.remove(self.get())


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
    def _add_enum(self, name, value):
        frame = Frame(self, height=40, width=300)
        label = Label(frame, text=name)
        variable = StringVar(frame)

        menu = OptionMenu(frame, variable, "True", "False", command=lambda event: self.input(event, name))
        menu.config(width=15, padx=0, pady=0)
        
        menu.pack(side='left', fill='y', expand=True)
        label.pack(side='left', fill='y', expand=True)
        frame.pack(side='top', anchor='nw')

        self._lines[name] = [frame, label, menu, variable]
        self._update_enum(name, value)

    def _update_enum(self, name, value):
        if value == '1':
            value = 'True'
        else:
            value = 'False'
        self._lines[name][3].set(value)


    def _add_entry(self, name, value):
        frame = Frame(self, height=40, width=300)
        label = Label(frame, text=name)
        entry = Entry(frame)

        entry.bind('<Return>', lambda event: self.input(event, name))
        entry.bind('<FocusOut>', lambda event: self.reset(event, name))

        entry.pack(side='left', fill='y', expand=True)
        label.pack(side='left', fill='y', expand=True)
        frame.pack(side='top', anchor='nw')

        self._lines[name] = [frame, label, entry]
        self._update_entry(name, value)

    def _update_entry(self, name, value):
        self._lines[name][2].delete(0, END)
        self._lines[name][2].insert(0, value)

    def _add_entry_list(self, name, value):
        frame = Frame(self)
        label = Label(frame, text=name)
        label.pack(side='top')
        frame.pack(side='top', anchor='nw')

        entry_list = dict()

        self._lines[name] = [frame, label, entry_list]
        self._update_list(name, value)

    def _update_list(self, name, value):
        list_rik = value.split(';')

        for rik in list_rik:
            if rik in self._lines[name][2]:
                # update
                self._lines[name][2][rik].delete(0, END)
                self._lines[name][2][rik].insert(0, rik)
            else:
                sub_address = rik.split('/')

                # go through parent
                previous = self
                for parent in sub_address[:-1]:
                    if parent not in self._lines[name][2]:
                        entry_list = EntryList(previous, parent)

                        self._lines[name][2][parent] = entry_list
                    previous = self._lines[name][2][parent]

                # create
                entry = EnumEntry(previous, rik)
                self._lines[name][2][rik] = entry

    def __init__(self, parent, frame, name, data="", config_type="None"):
        super().__init__(
            master=frame,
        )

        self.label = Label(self, text=name)
        self.label.pack(side='left', fill='y', expand=True)

        self._lines = dict()

        self._load_type(config_type, data)

        self.update(data)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def _load_type(self, type, data):
        stringables = ['String', 'IP', 'IPv4', 'IPv6', 'SerialPort', 'UserName', 'Password']
        stringables_settings = [
            ["Maximum Bytes", self._add_entry],
            ["Maximum Chars", self._add_entry],
            ["Hidden", self._add_entry]
        ]
        valueable = ['UInt8', 'UInt16', 'UInt32', 'Uint64', 'Int8', 'Int16', 'Int32', 'Int64', 'Real32', 'Real64',
                     'Numeric']
        valueable_settings = [
            ["Minimum", self._add_entry],
            ["Maximum", self._add_entry],
            ["Precision", self._add_entry],
            ["Is Float", self._add_enum],
            ["preUnit", self._add_entry],
            ["Unit", self._add_entry]
        ]

        multi_choice = ['MultiChoice']
        multi_choice_settings = [
            ["View Height", self._add_entry],
            ["Is Ordered", self._add_enum],
            ["Enum List", self._add_entry_list]
        ]

        self._lines = dict()
        data = data.split('|')

        settings = ''

        if type in stringables:
            settings = stringables_settings

        elif type in valueable:
            settings = valueable_settings

        elif type in multi_choice:
            settings = multi_choice_settings

        for setting in settings:
            if len(data) > 0:
                setting[1](setting[0], data.pop(0))
            else:
                setting[1](setting[0], '')

    def update(self, data):
        values = data.split('|')

        for name in self._lines:
            if len(values) != 0:
                my_value = values.pop(0)
            else:
                my_value = ''

            if isinstance(self._lines[name][2], OptionMenu):
                self._update_enum(name, my_value)
            elif isinstance(self._lines[name][2], dict):
                self._update_list(name, my_value)
            else:
                self._update_entry(name, my_value)

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

    def reset(self, event, name):
        values = self.old_data.split('|')
        index = list(self._lines).index(name)

        value = values[index]
    
        self._lines[name][2].delete(0, END)
        self._lines[name][2].insert(0, value)
