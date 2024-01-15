import json


class JSONStructure():
    def __init__(self, name="", filename =""):

        self.filename = filename
        self.json = None

        if filename != "":
            f = open(filename, "r")


            self.json = json.loads(f.read())
            f.close()
        else:
            self.json = {"name": name}

        print(self.json)


    def change_param(self, rel_path, data):
        pass



my_json = JSONStructure()