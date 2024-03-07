from tkinter import Frame, Button, Text, Entry, Menu
from source.frame.call import Call

class Name(Frame):

    def __init__(self, frame, name, parents = lambda empty_list: list(), func = lambda: print("button_pressed")):
        super().__init__(frame, width=150, height=30)

        self.pack_propagate(False)
        self.button = Button(
            self,
            text=name
        )

        self._parents = parents

        self.button.propagate(False)
        self.button.bind("<Button-1>", lambda w: func())
        self.button.bind("<Double-Button-1>", lambda w: self._show_entry())
        
        self.entry = Entry(self)
        self.entry.propagate(False)

        self.button.pack(fill='both', expand=True)
        
        self.grid(in_=frame, row=0, column=0, sticky='nw')

        #Add Menu
        self.popup = Menu(self, tearoff=0)

        #Adding Menu Items
        self.popup.add_command(label="Move Up", command= lambda: self.move_input("move_up"))
        self.popup.add_command(label="Move Down", command= lambda: self.move_input("move_down"))
        self.popup.add_separator()
        self.popup.add_command(label="New before", command= lambda: self.menu_input("add_before"))
        self.popup.add_separator()
        self.popup.add_command(label="Duplicate before", command= lambda: self.menu_input("duplicate_before"))
        self.popup.add_command(label="Duplicate at the end", command= lambda: self.menu_input("duplicate_end"))
        
        self.button.bind("<Button-3>", self.menu_popup)

    def _show_entry(self):
        self.entry.pack(fill='both', expand=True)
        self.entry.bind("<Leave>", self._hide_entry)
        self.entry.bind("<FocusOut>", self._hide_entry)
        self.entry.bind("<Return>", self.call_input)
        self.button.pack_forget()

    def _hide_entry(self, event):
        self.entry.pack_forget()
        self.entry.delete(0, 'end')
        self.entry.unbind('<Leave>')
        self.entry.unbind('<FocusOut>')
        self.entry.unbind('<Return>')
        self.button.pack(fill='both', expand=True)

    def call_set(self, value):
        self.button.configure(text=value)
        self.button.update()
        

    def call_input(self, event):
        value = self.entry.get()

        if value == '':
            self._hide_entry(None)
            return
        
        parents = []
        self._parents(parents)

        name = parents.pop(-1)

        Call.call(parents, name, value, 'update')

    def get(self):
        return self.button.cget('text')

    def menu_popup(self, event):
        # display the popup menu
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            #Release the grab
            self.popup.grab_release()

    def move_input(self, command):
        parents = list()
        self._parents(parents)
        Call.call(parents[:-1], parents[-1], None, command)

    def menu_input(self, command):
        parents = list()
        self._parents(parents)
        Call.call(parents[:-1], 'NewParameter', parents[-1], command)
