from tkinter import Frame, Label, Button


class WarningPopUp:
    def __init__(self, parents: list):
        self.parents = parents
        self.parents_color = []
        for parent in parents:
            self.parents_color.append(parent.cget('bg'))

        self.frame = None
        self.label = None
        self.icon = None
        self.status = False

    def warn(self, text):
        for parent in self.parents:
            parent.config(bg='red')
        self.status = True

        if self.frame is None:
            self.frame = Frame(self.parents[0].master)
            self.frame.pack(side='left')
            self.label = Label(self.frame, text=text)
            self.icon = Button(self.frame, text='i', command=self.info_show)
            self.icon.bind('<Leave>', self.info_hide)
            self.icon.pack(side='left')
        else:
            self.frame.pack(side='right')
            self.icon.pack(side='left')
            self.label.config(text=text)

    def clear(self):
        self.status = False

        if self.frame is not None:
            for parent, color in zip(self.parents, self.parents_color):
                parent.config(bg=color)
            self.info_hide()
            self.frame.pack_forget()

    def unload(self):
        if not self.status and self.frame is not None:
            self.frame.pack_forget()
            self.frame.destroy()
            self.frame = None
            self.label.pack_forget()
            self.label.destroy()
            self.label = None
            self.icon.pack_forget()
            self.icon.destroy()
            self.icon = None

    def info_show(self):
        self.label.pack(side='left')
        self.icon.config(command=self.info_hide)

    def info_hide(self, e=None):
        self.label.pack_forget()
        self.icon.config(command=self.info_show)
