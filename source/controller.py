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

        self.view.bind("<<load>>", self.load)

        self.view.bind("<<save_as>>", self.save)

        # self.model.file_load("test.json")
        # self.model.show(['content', 'properties','id'], 'userName', 'obis')

    def save(self, w):
        self.model.file_save(
            save_as()
        )

    def load(self, w):
        self.model.file_load(
            load()
        )
