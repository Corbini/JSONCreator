from source.frame.main import Main
from source.json_structure import JSONStructure
from source.window.file import load, save_as

class Controller():
    def __init__(self, view: Main, model: JSONStructure):
        self.view = view
        self.model = model
        self.connect_main_menu()

    def connect_main_menu(self):
        self.view.bind_all("<<quit>>", lambda w: self.view.master.destroy())

        self.view.bind("<<load>>", lambda w: load())

        self.view.bind("<<save_as>>", lambda w: save_as())
        print(self.view.event_info("<<save_as>>"))

