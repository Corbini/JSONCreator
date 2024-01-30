import json


class JSONStructure:
    def __init__(self, name="", filename=""):

        self.generate_object = lambda parents, name, data: print(parents, name, "\n", data, "\n")
        self.create_tree = lambda name: print(name)

        self.filename = filename
        self.json = None
        if filename != "":
            self.file_load(filename)
        else:
            self.json = {"name": name}

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
            sort_keys=True,
            indent=2
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

        self.json = json.loads(clean_data)

        self.create_tree(self.json['content']['device']['nameRik'])

        self.generate_tree(self.json['content']['properties'])

    def generate_tree(self, position, parents=list()):
        for node in position:
            if type(position[node]) is dict:
                self.generate_object(list(parents), node, None)
                parents.append(node)
                self.generate_tree(position[node], parents)
                parents.pop()
            else:
                self.generate_object(list(parents), node, position[node])

    def new_structure(self, name):
        device = {'nameRik': name}
        content = {'device': device}

        self.json = {'content': content}
        self.create_tree(name)

    def change_param(self, rel_path, data):
        pass
