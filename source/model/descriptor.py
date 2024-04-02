import json
from collections import OrderedDict
from copy import deepcopy
from source.model.conventer import clean_json
from source.model.undo_redo import UndoRedo
from source.model.oparation import Operation

class Descriptor:

    object_type = {}

    def __init__(self, name=""):

        self.generate_object = lambda parents, object_name, data: print(parents, object_name, "\n", data, "\n")
        self.remove_object = lambda parents, object_name: print(parents, object_name, "\n")
        self.create_tree = lambda object_name: print(object_name)
        self.reload_list = lambda parents, object_name, order_list: print(parents, object_name, "\n", order_list, "\n")
        self.warning = lambda parents, object_name, text: print(parents, object_name, "\n", "Warning: ")
        self.error = lambda parents, object_name, text: print(parents, object_name, "\n", "Error: ")

        self.json = None

        self.saves = UndoRedo(8)
        self.operation = Operation(self)

        self._path = ''
        self._name = ''

    @property
    def path(self):
        return self._path
    
    @property
    def name(self):
        return self._name

    def show(self, parents, object_name, content=''):
        data = self.json
        for parent in parents:
            data = data[parent]
        
        if content != '':
            print(data[content])
        else:
            print(data.keys())

    def data_get(self) -> json:
        clean_json(self.json['content'])

        return self.json

    def data_load(self, path, json_data: json):
        self._path = path

        self.json = json_data
        clean_json(self.json['content'])

        self._name = self.json['content']['device']['nameRik']
        self.create_tree(self._name)

        parents = [self._name]
        self.generate_tree(self.json['content']['properties'], parents)

    def generate_tree(self, position, parents=list()):
        for node in position:
            if type(position[node]) is OrderedDict:
                self.generate_object(list(parents), node, None)
                parents.append(node)
                self.generate_tree(position[node], parents)
                parents.pop()
            else:
                self.generate_object(list(parents), node, deepcopy(position[node]))

    def validate_tree(self, position, validate_position, parents=list(), keep_data=False, on_screen=True):
        sum_keys = []
        sum_keys += validate_position.keys()
        for key in position:
            if key not in sum_keys:
                sum_keys.append(key)

        for key in sum_keys:
            if key not in validate_position:
                # remove
                if on_screen:
                    self.remove_object(list(parents), key)

                position.pop(key)
                continue

            if key not in position:
                # new object
                position[key] = deepcopy(validate_position[key])

                if on_screen:
                    if type(position[key]) is OrderedDict:
                        self.generate_object(list(parents), key, None)
                        parents.append(key)
                        self.generate_tree(position[key], parents)
                        parents.pop()
                    else:
                        self.generate_object(list(parents), key, validate_position[key])

                continue

            if type(validate_position[key]) is not OrderedDict:
                if position[key] != validate_position[key] and not keep_data:
                    position[key] = validate_position[key]
                    self.generate_object(list(parents), key, deepcopy(position[key]))

                continue

            # update object
            if type(position[key]) is not OrderedDict:
                position[key] = deepcopy(validate_position[key])

                self.generate_object(list(parents), key, None)
                parents.append(key)
                self.generate_tree(position[key], parents)
                parents.pop()

            else:
                # parents.append(key)
                self.validate_tree(position[key], validate_position[key], parents + [key], keep_data)
                # parents.pop()

    def new_structure(self, name):
        self.json = OrderedDict([
            ("application", "golink"),
            ("type", "deviceDescriptor"),
            ("content", OrderedDict([
                ("device", OrderedDict([
                    ("nameRik", 'drv/' + name + '/name')
                ])),
                ("properties", OrderedDict([
                ]))
            ]))
        ])

        self.create_tree(self.json['content']['properties'])

    def undo(self):
        saved = self.saves.undo()

        if saved is None:
            return

        parents = [self._name]
        self.validate_tree(self.json['content']['properties'], saved['content']['properties'], parents)

    def redo(self):
        saved = self.saves.redo()

        if saved is None:
            return

        parents = [self._name]
        self.validate_tree(self.json['content']['properties'], saved['content']['properties'], parents)
