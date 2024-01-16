import json

class JSONStructure():
    def __init__(self, name="", filename =""):

        self.filename = filename
        self.json = None
        if filename != "":
            self.file_load(filename)
        else:
            self.json = {"name": name}

    def remove_comments(self, data):
        sequence = "//"

        clean_data = ''
        list = data.partition(sequence)
        clean_data += list[0]
        while (list[2] != ""):
            data_with_comment: str = list[2]

            data_without_comment = data_with_comment.partition("\n")[2]

            list = data_without_comment.partition(sequence)
            clean_data +=list[0]
        
        return clean_data

    def show(self, parents:list, parameter=''):
        data = self.json
        for parent in parents:
            data = data[parent]
        
        if parameter != '':
            print(data[parameter])
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

    def change_param(self, rel_path, data):
        pass
