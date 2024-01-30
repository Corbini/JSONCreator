from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry
from source.frame.setting import Setting


class Parameter(Frame):

    from ._frame_name import create_frame_name, change_name, configure_name
    from ._frame_generals import create_generals

    def __init__(self, parent, frame, name):
        super().__init__(
            master=frame,
            width=120,
            height=40,
            relief='sunken',
        )
        self.pack(side='top', anchor='nw')
        self.pack_propagate(True)

        self.par_parent = parent

        self.create_frame_name(name)
        self.create_generals()

        self.settings_view = Frame(self)

        self.settings_view.propagate(True)
        self.settings_list = dict()
        self.type = "int"

        self.settings_view.grid(row=1, column=1, sticky='nw')
        self.widen = False

    def change_size(self):
        if self.widen is False:

            self.settings_view.update()
            height = self.settings_view.winfo_height() + 30
            width = self.settings_view.winfo_width() + 220

            if height < 190:
                height = 190

            self.configure(
                height=height,
                width=1000
            )

            self.widen = True

        else:
            # self.settings_view.place_forget()

            self.configure(
                height=40,
                width=120
            )

            self.widen = False

    def set_type(self):
        self.type = "new_name"
        self.settings_list = dict()

    def update_setting(self, name, value):

        if name == "langPl":
            self.entry_2_t.insert(0, value)
            return

        if name == "langEn":
            self.entry_1_t.insert(0, value)
            return

        if name == "valueType":
            return

        if name not in self.settings_list:
            print("Create setting")
            self.settings_list[name] = Setting(self, self.settings_view, name, value)
        else:
            self.settings_list[name].update(value)

    def add_child(self, name):
        if name in self.settings_list:
            return

        print("Create parameter", name)
        self.settings_list[name] = Parameter(self, self.settings_view, name)
