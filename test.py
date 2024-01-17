from tkinter import Tk

from source.frame.parameter import Parameter
from source.window.main import MainWindow
from source.json_structure import JSONStructure


app = MainWindow()

parameter = Parameter(app, "licznik")
parameter.pack(side='top', anchor='nw')

def test(parents, name, value):
    parameter.add_setting(name, value)

model = JSONStructure()
model.generate_object = lambda parents, name, value: test(parents, name, value)
model.file_load("test.json")




app.mainloop()
