from source.frame.main import Main
from source.window.file import load, save_as, dir_path
from source.model.translation import Translation
from source.model.descriptor import Descriptor
from source.json_loader import data_load, data_save, data_type, dir_load
from source.frame.translation import Translation as FrameTranslation
from source.frame.call import Call
from source.frame.parameter._generals import General
from source.model.value_formats import ValueFormats
from source.model.oparation import Operation
from source.frame.settings.valueConfig import valueConfig


class Controller:
    def __init__(self, view: Main, model: Descriptor):
        self.view = view
        self.model = model
        self.languages_storage = dict()
        self.connect_main_menu()

    def connect_main_menu(self):
        Call.change_call(self.input)

        self.view.bind_all("<<quit>>", lambda w: self.view.master.destroy())

        self.view.bind("<<load>>", self.load)

        self.view.bind("<<save_as>>", self.save)
        self.view.bind("<<load_languages>>", self.load_languages)
        self.view.bind("<<save_languages>>", self.save_languages)
        self.view.bind_all('<<input>>', lambda w, data:self.input(w = data))

        object_valueConfig = data_load('assets/valueconfig_templates.json')
        valueConfig.template = object_valueConfig['content']
        ValueFormats.valueconfig_template = object_valueConfig['content']

        object_type = data_load('assets/type_templates.json')
        Operation.object_type = object_type['content']
        General.type_list = object_type['content']
        self.model.create_tree = lambda name: self.view.tree_create(name)
        self.model.generate_object = lambda parents, name, data: self.view.tree_update(parents, name, data)
        self.model.remove_object = lambda parents, name: self.view.tree_remove(parents, name)
        self.model.reload_list = lambda parents, name, list: self.view.tree_reload_list(parents, name, list)
        ValueFormats.call_error = lambda parents, name, text: self.view.tree_data_error(parents, name, text)
        ValueFormats.object_type = object_type['content']

        self.view.bind("<<tree_new>>", lambda w: self.model.new_structure("new_tree"))
        self.view.bind_all("<Control-z>", lambda event: self.model.undo())
        self.view.bind_all("<Control-y>", lambda event: self.model.redo())

    def save(self, w):
        path = save_as()

        data = self.model.data_get()

        data_save(path, data)

    def load(self, w):
        path = load()

        if path == '':
            return 

        data = data_load(path)

        match data_type(data):
            case 'deviceDescriptor':
                self.model.data_load(path, data)
            case 'languageDefinition':
                self.load_language(path, data)

    def input(self, parents, name, value, operation):
        if name in self.languages_storage:
            self.languages_storage[name].call(parents, value, operation)
        else:
            self.model.operation.input(parents, name, value, operation)

    def load_language(self, path, data_json):

        translation = Translation()
        translation.generate_object = lambda parents, name, data: self.view.tree_update(parents, name, data)

        if translation.data_load(path, data_json):
            self.languages_storage[translation.name] = translation
            print("Language: ", translation.name, ", Loaded")

        FrameTranslation.names = self.languages_storage.keys()
    
    def load_languages(self, e):
        path = dir_path()
        loaded_path = list()
        language_list = dir_load(path)

        for data in language_list:
            if data_type(data[1]) == 'languageDefinition':
                self.load_language(data[0], data[1])

    def save_languages(self, e):
        for language_name in self.languages_storage:
            filepath = self.languages_storage[language_name].filepath
            data = self.languages_storage[language_name].data_get()

            data_save(filepath, data)