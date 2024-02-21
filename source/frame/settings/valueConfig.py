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

    def __init__(self, parent, frame, name, data=""):
        super().__init__(
            master=frame,
        )

        self.label = Label(self, text= name)
        self.label.pack(side='left', fill='y', expand=True)

        values = data.split('|')

        self._lines = dict()
        self._add_entry("Minimum", values[0])
        self._add_entry("Maximum", values[1])
        self._add_entry("Scaler", values[2])
        self._add_enum("isFloat", values[3])
        self._add_entry("Unit", values[4])

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def update(self, data):
        values = data.split('|')

        for value in self._lines:
            if isinstance(self._lines[value][2], OptionMenu):
                if isinstance(value, bool):
                    if value:
                        self._lines[value][3].set('True')
                    else:
                        self._lines[value][3].set('False')
                else:
                    self._lines[value][3].set(values.pop(0))
            else:
                self._lines[value][2].delete(0, END)
                self._lines[value][2].insert(0, values.pop(0))

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
