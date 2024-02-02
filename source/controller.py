from source.frame.main import Main
from source.json_structure import JSONStructure
from source.window.file import load, save_as


class Controller:
    def __init__(self, view: Main, model: JSONStructure):
        self.view = view
        self.model = model
        self.connect_main_menu()

    def connect_main_menu(self):
        self.view.bind_all("<<quit>>", lambda w: self.view.master.destroy())

        self.view.bind("<<load>>", self.load)

        self.view.bind("<<save_as>>", self.save)
        self.view.bind_all('<<input>>', lambda w, data:self.input(w = data))

        self.model.create_tree = lambda name: self.view.tree_create(name)
        self.model.generate_object = lambda parents, name, data: self.view.tree_update(parents, name, data)

        self.view.bind("<<tree_new>>", lambda w: self.model.new_structure("new_tree"))
        self.view.tree_input_set(lambda object, parents, name, value, operation: self.input(parents, name, value, operation))
        self.view.bind_all("<Control-z>", lambda event: self.model.load_last())


    def save(self, w):
        self.model.file_save(
            save_as()
        )

    def load(self, w):
        self.model.file_load(
            load()
        )

    def input(self, parents, name, value, operation):
        status = self.model.change_param(parents, name, value, operation)
