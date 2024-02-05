import json
from collections import OrderedDict
from copy import deepcopy

class JSONStructure:
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

    @staticmethod
    def remove_comments(data):
        sequence = "//"

        clean_data = ''
        data_buffer = data.partition(sequence)
        clean_data += data_buffer[0]
        while data_buffer[2] != "":
            data_with_comment: str = data_buffer[2]
            data_buffer = data_with_comment.partition("\n")[2]
            data_buffer = data_buffer.partition(sequence)
            clean_data += data_buffer[0]
        
        return clean_data

    def show(self, parents, object_name, content=''):
        data = self.json
        for parent in parents:
            data = data[parent]
        
        if content != '':
            print(data[content])
        else:
            print(data.keys())

    def remove_empty_settings(self, parent):
        for child in parent:
            if isinstance(parent[child], OrderedDict):
                self.remove_empty_settings(parent[child])
            elif parent[child] == '':
                parent.pop(child)

    def file_save(self, filename: str):
        self.remove_empty_settings(self.json)

        file = open(filename, "w")

        text = json.dumps(
            obj=self.json,
            indent=2,
            ensure_ascii=False
        )
        
        file.write(text)
        file.close()

    def file_load(self, filename: str):
        f = open(filename, "r")

        if f.closed:
            print("File not opened")
            return

        data = f.read()
        f.close()

        clean_data = self.remove_comments(data)

        self.json = json.loads(clean_data, object_pairs_hook=OrderedDict)

        self.create_tree(self.json['content']['device']['nameRik'])

        self.generate_tree(self.json['content']['properties'])

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
                    ("nameRik", 'drv/g35Pge308k/' + name + '/name')
                ])),
                ("properties", OrderedDict([
                ]))
            ]))
        ])

        self.create_tree(self.json['content']['properties'])

    def change_param(self, rel_path, name, data, operation) -> bool:
        self.last_operations()
        path = self.json['content']['properties']

        for object in rel_path:
            path = path[object]


        match operation:
            case 'remove':
                path.pop(name)

            case 'read':
                if name in path:    
                    data = path[name]
                else:
                    data = ''

            case 'add':
                if name in path:
                    return
                
                self.add_child(rel_path, name, data, path)

            case _:
                if self.value_checker(name, data):
                    if name not in path:
                       path[name] = data
                    
                    elif isinstance(path[name], OrderedDict):
                        if name == data:
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
                    data = path[name]
        

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


    def value_checker(self, name, value) -> bool:
        match name:
            case 'valueType':
                return value in ['Branch', 'UInt64', "String","DateTime","UInt8","UInt16","UInt32","UInt64","Int8","Int16","Int32","Int64","Real32","Real64","Boolean","UserName","Password","SerialPort","IP","IPv4","IPv6"]
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
                object[setting] = ''
                self.generate_object(rel_path, setting, '')

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