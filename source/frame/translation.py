from tkinter import Frame, Entry, Label, Text, Button, END, OptionMenu, StringVar
from source.frame.call import Call


class Translation:
    names = []

    def __init__(self, frame = None, parents = lambda empty_list: list()):
        self._languages = dict()
        self._frame = frame
        self.parents = parents

        for name in self.names:
                self._add_language(name)
    
    def reload_language(self):
        for name in self.names:
            if name not in self._languages:
                self._add_language(name)

            self.call_get(name)

    def _add_language(self, name):
        label = Label(self._frame, text='język '+name)
        label.pack(side='top',fill='x', expand=True)
        entry = Entry(self._frame)
        entry.bind('<Return>', lambda event: self.call_input(name, event))
        entry.bind('<FocusOut>', lambda event: self.call_get(name))
        entry.pack(side='top',fill='x', expand=True)
        entry.language_name = name
        self._languages[name] = [label, entry]
        
    def call_set(self, name, value):
        if name not in self._languages:
            self._add_language(name)

        self._languages[name][1].delete(0, END)
        self._languages[name][1].insert(0, value)

    def call_get(self, name):
        parents = []
        self.parents(parents)

        Call.call(parents, name, None, 'get')

    def call_input(self, name, event):
        parents = []
        self.parents(parents)
        text = event.widget.get()

        Call.call(parents, name, text, 'set')

    def color(self, name, color):
        self._languages[name][1].configure(bg=color)
