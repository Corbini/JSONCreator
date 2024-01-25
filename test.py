from tkinter import Tk

from source.frame.parameter import Parameter
from source.window.main import MainWindow
from source.json_structure import JSONStructure


app = MainWindow()

parameter = Parameter(None, app, "properties")
parameter.pack(side='top', anchor='nw')


model = JSONStructure()
model.generate_object = lambda parents, name, value: parameter.update(parents, name, value)
model.file_load("test.json")

app.mainloop()
