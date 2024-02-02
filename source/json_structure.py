import json
from collections import OrderedDict
from copy import deepcopy

class JSONStructure:
    def __init__(self, name="", filename=""):

        self.generate_object = lambda parents, name, data: print(parents, name, "\n", data, "\n")
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

    def file_save(self, filename: str):
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
        if self.value_checker(name, data) is False:
            return
        
        self.last_operations()
        path = self.json['content']['properties']

        for object in rel_path:
            path = path[object]

        if operation == 'remove':
            path.pop(name)
        else:
            path[name] = data
        
        self.generate_object(rel_path, name, data)


    def value_checker(self, name, value) -> bool:
        return True
    
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