import json
from source.window.file import load, save_as
from source.window.main import MainWindow

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

        self.file_load("C:/Users/PatrykStrama/Desktop/python projects/JSONCreator/elgamaDrivers0001g35pge308k2022.json")

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


            


    def file_load(self, filename: str):
        f = open(filename, "r")

        if f.closed:
            print("File not opened")
            return

        data = f.read()
        f.close()

        # print(data)

        clean_data = self.remove_comments(data)

        self.json = json.loads(clean_data)

        print(self.json)

    def save_as(self, filename: str):
        pass

    def change_param(self, rel_path, data):
        pass



my_json = JSONStructure()

my_json.file_load("C:/Users/PatrykStrama/Desktop/python projects/JSONCreator/elgamaDrivers0001g35pge308k2022.json")