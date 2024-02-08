from source.frame.main import Main
from source.window.file import load, save_as
from source.model.translation import Translation
from source.model.descriptor import Descriptor
from source.json_loader import data_load, data_save, data_type

class Controller:
    def __init__(self, view: Main, model: Descriptor):
        self.view = view
        self.model = model
        self.languages_storage = dict()
        self.connect_main_menu()

    def connect_main_menu(self):
        self.view.bind_all("<<quit>>", lambda w: self.view.master.destroy())

        self.view.bind("<<load>>", self.load)

        self.view.bind("<<save_as>>", self.save)
        self.view.bind_all('<<input>>', lambda w, data:self.input(w = data))

        self.model.create_tree = lambda name: self.view.tree_create(name)
        self.model.generate_object = lambda parents, name, data: self.view.tree_update(parents, name, data)
        self.model.remove_object = lambda parents, name: self.view.tree_remove(parents, name)

        self.view.bind("<<tree_new>>", lambda w: self.model.new_structure("new_tree"))
        self.view.tree_input_set(lambda object, parents, name, value, operation: self.input(parents, name, value, operation))
        self.view.tree_languages_set(lambda e: self.languages())
        self.view.bind_all("<Control-z>", lambda event: self.model.load_last())

    def save(self, w):
        path = save_as()

        data = self.model.data_get()

        data_save(path, data)

    def load(self, w):
        path = load()

        data = data_load(path)

        match data_type(data):
            case 'deviceDescriptor':
                self.model.data_load(data)
            case 'languageDefinition':
                self.load_language(data)

    def input(self, parents, name, value, operation):
        if name in self.languages():
            self.languages_storage[name].call(parents, value, operation)
        else:
            self.model.change_param(parents, name, value, operation)

    def load_language(self, data):

        translation = Translation()
        translation.generate_object = lambda parents, name, data: self.view.tree_update(parents, name, data)

        if translation.data_load(data):
            self.languages_storage[translation.name] = translation
            print("Language: ", translation.name, ", Loaded")

    def languages(self):
        return self.languages_storage.keys()
    