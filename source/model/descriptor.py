import json
from collections import OrderedDict
from copy import deepcopy

class Descriptor:

    object_type= {}


    def __init__(self, name="", filename=""):

        self.generate_object = lambda parents, name, data: print(parents, name, "\n", data, "\n")
        self.remove_object = lambda parents, name: print(parents, name, "\n")
        self.create_tree = lambda name: print(name)

        self.filename = filename
        self.json = None
        if filename != "":
            self.file_load(filename)
        else:
            self.json = None

        self.saves = list()

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

    def object_make_valueConfig(self, object: OrderedDict):
        # [valueMinimum, valueMaximum, valueScaler, if_float, valueUnit]
        value_list = ['','','','','']
        
        if 'valueConfig' in object:
            value_list = object['valueConfig'].split('|')


        key_list = list(object.keys())
        for key in key_list:
            match key:
                case 'minValue':
                    value_list[0] = object[key]
                    object.pop(key)
                case 'valueMinimum':
                    value_list[0] = object[key]
                    object.pop(key)
                case 'maxValue':
                    value_list[1] = object[key]
                    object.pop(key)
                case 'valueMaximum':
                    value_list[1] = object[key]
                    # object.pop(key)
                case 'unit':
                    value_list[4] = object[key]
                    object.pop(key)
                case 'valueUnit':
                    value_list[4] = object[key]
                    object.pop(key)

        value_config = ""
        value_config += str(value_list[0])

        for value in value_list[1:]:
            value_config += '|'
            value_config += str(value)

        object['valueConfig'] = value_config

    def clean_json(self, parent):
        childs = list(parent.keys())

        rename_childs = {'maxValue': 'valueMaximum', 'minValue': 'valueMinimum', 'defaultValue': 'valueDefault', 'access': 'valueAccess', 'type': 'valueType', 'unit': 'valueUnit', 'lenght': 'valueMaximum'}
                         # 'branch': 'Branch', 'string': 'String', 'dateTime': 'DataTime', 'boolean': 'Boolean', 'int16': "Int16"}
        incorrect_names = ['langEn', 'langPl']

        to_valueConfig = ['valueMinimum', 'valueMaximum', 'valueUnit']

        for child in childs:
            if isinstance(parent[child], OrderedDict):
                self.clean_json(parent[child])
            elif parent[child] == '':
                parent.pop(child)
            elif parent[child] == 'RW':
                parent.pop(child)
            elif child in rename_childs.keys():
                parent[rename_childs[child]] = parent.pop(child)
            elif child in incorrect_names:
                parent.pop(child)

        for child in childs:
            if child in to_valueConfig:
                self.object_make_valueConfig(parent)

    def data_get(self) -> json:
        self.clean_json(self.json['content'])

        return self.json

    def data_load(self, path, json_data: json):

        self._path = path

        self.json = json_data
        self.clean_json(self.json['content'])

        self._name = self.json['content']['device']['nameRik']
        self.create_tree(self._name)

        parents = []
        parents.append(self._name)
        self.generate_tree(self.json['content']['properties'], parents)

    def generate_tree(self, position, parents=list()):
        for node in position:
            if type(position[node]) is OrderedDict:
                self.generate_object(list(parents), node, None)
                parents.append(node)
                self.generate_tree(position[node], parents)
                parents.pop()
            else:
                self.generate_object(list(parents), node, position[node])

    def validate_tree(self, position, validate_position, parents=list(), keep_data=False, on_screen=True):

        nodes = list(validate_position.keys())
        for key in position:
            if key not in nodes:
                nodes.append(key)
        # nodes = set(list(validate_position.keys()) + list(position.keys()))

        for node in nodes:
            if node in validate_position and node in position:

                #update
                if type(validate_position[node]) is OrderedDict:
                    if type(position[node]) is not OrderedDict:
                        position[node] = deepcopy(validate_position[node])

                        if on_screen:
                            self.generate_object(list(parents), node, None)
                            parents.append(node)
                            self.generate_tree(position[node], parents)
                            parents.pop()

                    else:
                        parents.append(node)
                        self.validate_tree(position[node], validate_position[node], parents, keep_data, on_screen)
                        parents.pop()

                elif position[node] != validate_position[node] and not keep_data:
                    position[node] = validate_position[node]

                    if on_screen:
                        self.generate_object(list(parents), node, position[node])


            elif node not in position:
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

    def change_param(self, rel_path, name, data, operation) -> bool:
        self.last_operations()
        path = self.json['content']['properties']

        

        for object in rel_path[1:]:
            path = path[object]


        match operation:
            case 'remove':
                path.pop(name)
                self.remove_object(rel_path, name)

            case 'read':
                if name in path:    
                    data = path[name]
                else:
                    data = ''
                    
                self.generate_object(rel_path, name, data)

            case 'add':
                if name in path:
                    return
                
                self.add_child(rel_path, name, data, path)

                self.generate_object(rel_path, name, data)

            case _:
                if self.value_checker(name, data):
                    if name not in path:
                       path[name] = data
                    
                    elif isinstance(path[name], OrderedDict):
                        if name == data:
                            return 
                        
                        if data in path:
                            return
                        
                        keys = list(path.keys())
                        keys[keys.index(name)] = data
                        path[data] = path.pop(name)

                        flag = False
                        for key in keys:
                            if flag:
                                path.move_to_end(key)
                            elif key == data:
                                flag=True

                        rel_path.append(name)
                        name = 'name'
                    else:
                        path[name] = data

                    if name == 'valueType':
                        self.change_type(rel_path, path, data)
                else:
                    if name in path:
                        data = path[name]
                    else:
                        data = ''
            
                self.generate_object(rel_path, name, data)
        


    def add_child(self, path, name, data='', parent=None):
        if parent is None:
            parent = self.json['content']['properties']
            for _parent in path:
                parent = parent[_parent]

        if data is None:
            parent[name] = OrderedDict()
            self.generate_object(path, name, data)
            
            new_path = path + [name]
            self.add_child(new_path, 'valueType', 'Branch', parent[name])
            for setting in self.object_type['Branch'][1:]:
                self.add_child(new_path, setting, '', parent[name])
        else:
            parent[name] = data
            self.generate_object(path, name, data)

    def is_unsigned_int(self, value, max_value = 20000) -> bool:
        if not value.isdigit():
            return False
                
        if int(value) < 0 or int(value) > max_value:
            return False
        
        return True


    def value_checker(self, name, value: str) -> bool:
        match name:
            case 'valueType':
                return value in self.object_type
            case 'valueMaximum':
                return self.is_unsigned_int(value)
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
        childs = list(object.keys())
        if object_type in self.object_type:
            acceptable_settings = self.object_type[object_type]
        else:
            acceptable_settings = self.object_type['Branch']

        if object_type == "Branch":
            for child in childs:
                if not isinstance(object[child], OrderedDict):
                    if child in acceptable_settings:
                        continue

                    object.pop(child)
                    self.remove_object(rel_path, child)
        else:
            if object_type == object['valueType']:
                self.validate_tree(object, self.object_type[object_type], rel_path, True)
            else:
                self.validate_tree(object, self.object_type[object_type], rel_path)

    def last_operations(self):
        if len(self.saves) >=8:
            self.saves.pop()

        self.saves.insert(0, deepcopy(self.json))

    def load_last(self):
        if len(self.saves) < 1:
            return
        
        save = self.saves.pop(0)
        
        parents = []
        parents.append(self._name)
        self.validate_tree(self.json['content']['properties'], save['content']['properties'], parents)
