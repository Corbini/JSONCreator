import json
from collections import OrderedDict
from copy import deepcopy

class Descriptor:
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

    def clean_json(self, parent):
        childs = list(parent.keys())

        rename_childs = {'maxValue': 'valueMaximum', 'minValue': 'valueMinimum', 'defaultValue': 'valueDefault', 'access': 'valueAccess', 'type': 'valueType', 'unit': 'valueUnit', 'lenght': 'valueMaximum'}
                         # 'branch': 'Branch', 'string': 'String', 'dateTime': 'DataTime', 'boolean': 'Boolean', 'int16': "Int16"}
        incorrect_names = ['langEn', 'langPl']

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
            for setting in self._acceptable_settings['Branch'][1:]:
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
                return value in ['Branch', 'UInt64', "String","DateTime","UInt8","UInt16","UInt32","UInt64","Int8","Int16","Int32","Int64","Real32","Real64","Boolean","UserName","Password","SerialPort","IP","IPv4","IPv6"]
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

    _acceptable_settings = {
        'Branch': ['valueType', 'readOnOpen'],
        'String': ['valueType', 'obis', 'valueAccess', 'valueDefault', 'valueMinimum', 'valueMaximum'], # valueMin/valueMaximum is the min and max lenght
        'Boolean': ['valueType', 'obis', 'valueAccess', 'valueDefault'],
        'DataTime': ['valueType', 'obis', 'valueAccess', 'valueInitial'],
        'SerialPort': ['valueType'],
        'IP': ['valueType', 'obis', 'valueAccess'],
        'IPv4': ['valueType', 'obis', 'valueAccess'],
        'IPv6': ['valueType', 'obis', 'valueAccess'],
        'UserName': ['valueType', 'obis', 'valueAccess', 'valueMinimum', 'valueMaximum'],
        'password': ['valueType', 'obis', 'valueAccess', 'valueMinimum', 'valueMaximum'],
        'UInt8':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'UInt16':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'UInt32':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'UInt64':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Int8':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Int16':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Int32':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Int64':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Real32':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],
        'Real64':['valueType', 'obis', 'valueAccess', 'valueDefault','valueMinimum', 'valueMaximum'],

    }

    def change_type(self, rel_path, object: OrderedDict, object_type):
        childs = list(object.keys())
        if object_type in self._acceptable_settings:
            acceptable_settings = self._acceptable_settings[object_type]
        else:
            acceptable_settings = self._acceptable_settings['Branch']

        if object_type == "Branch":
            for child in childs:
                if not isinstance(object[child], OrderedDict):
                    if child in acceptable_settings:
                        continue

                    object.pop(child)
                    self.remove_object(rel_path, child)
        else:
            for child in childs:
                if child in acceptable_settings:
                    continue

                object.pop(child)
                self.remove_object(rel_path, child)

        for setting in acceptable_settings:
            if setting not in object:
                self.add_child(rel_path, setting, '', object)
                # object[setting] = ''
                # self.generate_object(rel_path, setting, '')

        pass

    def last_operations(self):
        if len(self.saves) >=8:
            self.saves.pop()

        self.saves.insert(0, deepcopy(self.json))

    def load_last(self):
        if len(self.saves) < 1:
            return
        
        save = self.saves.pop(0)
        self.json = save
        self.create_tree(self.json['content']['device']['nameRik'])
        self.generate_tree(self.json['content']['properties'])