from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar, Event, Button
from source.frame.call import Call


class valueEnum(Frame):
    def __init__(self, parent, frame, name, value_list=None):
        super().__init__(
            master=frame,
        )

        self.label = Label(self, text=name)
        self.label.pack(side='left', fill='y', expand=True)

        if value_list is None:
            value_list = list('first_enum')
        self.old_values = list(value_list)

        self._entries = list()
        index = 0
        while len(value_list) > 0:
            self.add_entry(value_list.pop(0), index)
            index += 1

        self.par_parent = parent

        self.addable = Button(self, text='add', command=self.call_add)

        self.addable.pack(side='right', anchor='nw')

        self.pack(side='top', anchor='nw')

    def add_entry(self, value, index):
        entry = Entry(self)
        entry.insert(0, value)
        entry.bind('<Return>', lambda event: self.input(event, index))
        entry.bind('<FocusOut>', lambda event: self.reset(event, index))
        entry.pack(side='left', fill='y', expand=True)
        self._entries.append(entry)

    def update(self, data_list):
        over_sized = len(self.old_values) - len(data_list)
        while over_sized > 0:
            over_sized -= 1
            self._entries.pop(-1)

        self.old_values = list(data_list)

        for entry in self._entries:
            entry.delete(0, END)
            entry.insert(0, data_list.pop(0))

        while len(data_list) > 0:
            self.add_entry(data_list.pop(0), len(self._entries))

    def call_add(self):
        if self.par_parent is None:
            return

        parents = list()
        self.par_parent.get_parent(parents)

        new_values = list(self.old_values)
        new_values.append("new")

        name = self.label.cget("text")
        Call.call(parents, name, new_values, 'change')

    def input(self, event: Event, index: int):
        if self.par_parent is None:
            return

        parents = list()
        self.par_parent.get_parent(parents)

        new_values = list(self.old_values)
        new_values[index] = event.widget.get()

        name = self.label.cget("text")

        Call.call(parents, name, new_values, 'change')

    def reset(self, event: Event, index: int):
        value = self.old_values[index]

        event.widget.delete(0, END)
        event.widget.insert(0, value)
