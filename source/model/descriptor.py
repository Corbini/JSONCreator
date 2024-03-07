import json
from collections import OrderedDict
from copy import deepcopy
from source.model.conventer import clean_json
from source.model.undo_redo import UndoRedo
# from source.model.value_formats import ValueFormats


class Descriptor:

    object_type= {}


    def __init__(self, name="", filename=""):

        self.generate_object = lambda parents, name, data: print(parents, name, "\n", data, "\n")
        self.remove_object = lambda parents, name: print(parents, name, "\n")
        self.create_tree = lambda name: print(name)
        self.reload_list = lambda parents, name, list: print(parents, name, "\n", list, "\n")

        self.filename = filename
        self.json = None
        if filename != "":
            self.file_load(filename)
        else:
            self.json = None

        self.saves = UndoRedo(8)

        # self.checker = ValueFormats()

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
        nodes = list(validate_position.keys())
        for key in position:
            if key not in nodes:
                nodes.append(key)

        for node in nodes:
            if node in validate_position and node in position:
                #update object
                if type(validate_position[node]) is OrderedDict:
                    if type(position[node]) is not OrderedDict:
                        position[node] = deepcopy(validate_position[node])

                        self.generate_object(list(parents), node, None)
                        parents.append(node)
                        self.generate_tree(position[node], parents)
                        parents.pop()

                    else:
                        parents.append(node)
                        self.validate_tree(position[node], validate_position[node], parents, keep_data)
                        parents.pop()

                elif position[node] != validate_position[node] and not keep_data:
                    position[node] = validate_position[node]
                    self.generate_object(list(parents), node, deepcopy(position[node]))

            elif node not in position:
                #new object
                position[node] = deepcopy(validate_position[node])

                if on_screen:
                    if type(position[node]) is OrderedDict:
                        self.generate_object(list(parents), node, None)
                        parents.append(node)
                        self.generate_tree(position[node], parents)
                        parents.pop()
                    else:
                        self.generate_object(list(parents), node, validate_position[node])

            else:
                # remove
                if on_screen:
                    self.remove_object(list(parents), node)

                position.pop(node)

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

    def change_param(self, rel_path: list, name, data, operation) -> bool:
        self.saves.save(self.json)
        parent = self.json['content']['properties']

        for object in rel_path[1:]:
            parent = parent[object]

        match operation:
            case 'remove':
                parent.pop(name)
                self.remove_object(rel_path, name)


    def _go_to_parent(self, parents):
        parent = self.json['content']['properties']

        try:
            for object in parents[1:]:
                parent = parent[object]
        except:
            print("Incorrect parents")
            return None

        return parent

    def remove(self, parents, name, data):
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        if name not in parent:
            return False

        self.saves.save(self.json)
        parent.pop(name)
        self.remove_object(parents, name)
        return True

    def read(self, parents, name, data):
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        if name not in parent:
            self.generate_object(parents, name, '')
            return False

        self.generate_object(parents, name, parent[name])

        return True

    def move_before(self, object, move_name, before_name):
        sort_list = list(object.keys())
        first = sort_list.index(before_name)

        sort_list = sort_list[first:]
        sort_list.pop(sort_list.index(move_name))

        for object_name in sort_list:
            object.move_to_end(object_name)

    def move_up(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        self.saves.save(self.json)
        sort_list = list(parent.keys())
        before = sort_list.index(name) - 1
        if before < 0:
            return False

        self.move_before(parent, name, sort_list[before])

        updates_list = list(parent.keys())
        updates_list.remove('valueType')
        self.reload_list(parents, name, updates_list)

        return True

    def move_down(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        self.saves.save(self.json)
        sort_list = list(parent.keys())
        before = sort_list.index(name) + 1
        if before < 0:
            return False

        self.move_before(parent, sort_list[before], name)

        updates_list = list(parent.keys())
        updates_list.remove('valueType')
        self.reload_list(parents, name, updates_list)

        return True

    def add_before(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        if name in parent:
            print("Object have: ", name)
            return False

        self.saves.save(self.json)
        self.add_child(parents, name, data, parent)
        self.generate_object(parents, name, data)

        self.move_before(parent, name, data)

        updates_list = list(parent.keys())
        updates_list.remove('valueType')
        self.reload_list(parents[:-1], parents[-1], updates_list)

        return True

    def add(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        if name in parent:
            print("Object have: ", name)
            return False

        self.saves.save(self.json)
        self.add_child(parents, name, data, parent)
        self.generate_object(parents, name, data)

        return True

    def _duplicate(self, parents, name, data, parent):
        parent[name] = deepcopy(parent[data])
        self.generate_object(parents, name, None)
        parents.append(name)
        self.generate_tree(parent[name], parents)

    def duplicate_before(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        new_name = data + '_duplicate'
        if new_name in parent:
            print("Object have: ", name)
            return False

        self.saves.save(self.json)
        self._duplicate(parents, new_name, data, parent)

        self.move_before(parent, new_name, data)

        updates_list = list(parent.keys())
        updates_list.remove('valueType')
        self.reload_list(parents[:-1], parents[-1], updates_list)

        return True

    def duplicate_end(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        new_name = data + '_duplicate'
        if new_name in parent:
            print("Object have: ", name)
            return False

        self.saves.save(self.json)
        self._duplicate(parents, new_name, data, parent)

        return True

    def update(self, parents, name, data) -> bool:
        parent = self._go_to_parent(parents)
        if parent is None:
            return False

        self.saves.save(self.json)
        # Checks if value is correct
        if not self.value_checker(parent, name, data):
        # if not self.checker.check(data, name):
            # reset data to last correct value
            if name in parent:
                self.generate_object(parents, name, parent[name])
            else:
                self.generate_object(parents, name, '')

            return False

        if isinstance(parent[name], OrderedDict):
            # Rename object
            if name == data:
                return False

            if data in parent:
                return False

            keys = list(parent.keys())
            keys[keys.index(name)] = data
            parent[data] = parent.pop(name)

            flag = False
            for key in keys:
                if flag:
                    parent.move_to_end(key)
                elif key == data:
                    flag = True

            parents.append(name)
            name = 'name'
        else:
            parent[name] = deepcopy(data)
            if name == 'valueType':
                self.change_type(parents, parent, data)


        self.generate_object(parents, name, data)
        return True

    def add_child(self, path, name, data='', parent=None):
        if parent is None:
            parent = self.json['content']['properties']
            for _parent in path:
                parent = parent[_parent]

        if data is None:
            parent[name] = OrderedDict()
            self.generate_object(path, name, data)
            
            new_path = path + [name]
            # self.add_child(new_path, 'valueType', 'Branch', parent[name])
            
            model = self.object_type['Branch']
            for setting in model:
                self.add_child(new_path, setting, model[setting], parent[name])
        else:
            parent[name] = data
            self.generate_object(path, name, data)


    def is_unsigned_int(self, value, max_value = 50000) -> bool:
        if not value.isdigit():
            return False
                
        if int(value) < 0 or int(value) > max_value:
            return False
        
        return True


    def value_checker(self, parent, name, value: str) -> bool:
        match name:
            case 'valueType':
                return value in self.object_type
            case 'valueMaximum':
                if not self.is_unsigned_int(value):
                    return False

                if 'valueMinimum' in parent:
                    return value > parent['valueMinimum']

                return True

            case 'valueMinimum':
                return self.is_unsigned_int(value)
            case 'valueUnit':
                return True # value in ['ms', 's', 'min', 'hour', 'mV', 'V', 'MV',  'mA', 'A', 'MA', 'Wh', 'kWh', 'MWh', 'varh', 'kvarh', 'Mvarh', 'Degree', 'C', 'F', 'percent', 'Hz', 'VA', 'kVA', 'MVA']
            case 'obis':
                seperated_class = value.split(':')
                if len(seperated_class) != 2:
                    print('Incorrect amount of class')
                    return False
                if self.is_unsigned_int(seperated_class[0]) is False:
                    print('Incorrect format of class')
                    return False

                seperated_atribute = seperated_class[1].split(';')
                if len(seperated_atribute) != 2:
                    print('Incorrect amount of atribute')
                    return False
                if self.is_unsigned_int(seperated_atribute[1]) is False:
                    print('Incorrect format of atribute')
                    return False

                obis = seperated_atribute[0].split('.')

                if len(obis) != 6:
                    print('Incorrect amount of obis numbers')
                    return False
                for number in obis:
                    if self.is_unsigned_int(number, 255) is False:
                        print('Incorrect format of obis numbers')
                        return False

                return True

            case _:
                return True

    def change_type(self, rel_path, object: OrderedDict, object_type):
        if object_type not in self.object_type:
            return

        if object_type == "Branch":
            children = list(object.keys())
            acceptable_settings = self.object_type[object_type]

            for child in children:
                if not isinstance(object[child], OrderedDict) and child not in acceptable_settings:
                    object.pop(child)
                    self.remove_object(rel_path, child)

        else:
            data_keep = object_type == object['valueType']
            self.validate_tree(object, self.object_type[object_type], rel_path, data_keep)

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
