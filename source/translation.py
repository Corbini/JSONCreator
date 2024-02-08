import json

class Translations:
    
    generate_object = lambda self, parents, name, data: print(parents, name, data)

    def __init__(self):
        self._filename = ''

        self._name = ''
        self._translations = dict()

    @property
    def name(self):
        return self._name

    def create(self, filename, name):
        self._name = name
        self._translations = dict()

        print('Program wants to create ', name, ' language in file: ', filename)

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

    def load(self, filename) -> bool:
        file = open(filename, "r", encoding="utf8")

        if file.closed:
            print("File not opened")
            return

        data = file.read()
        file.close()

        data = self.remove_comments(data)

        json_data = json.loads(data)

        if json_data['type'] !='languageDefinition':
            return False

        self._name = json_data['content']['name']
        encoded = json_data['content']['translations']
        self._translations = self._decode(encoded)
        return True

    def save(self, filename):
        encoded = self._encode()

        json_data = json({'application': 'golink', 'type': 'languageDefinition', 'content': {'name': self._name, 'translations': encoded}})

        
        file = open(filename, "w")

        if file.closed:
            return

        text = json_data.dumps(
            obj=self.json,
            indent=2,
            ensure_ascii=False
        )
        
        file.write(text)
        file.close()

    def _encode(self) -> list:
        encoded = list()

        for key in self.translations.keys():
            encoded.append(str(key + self._translations[key]))

        return encoded
    
    def _decode(self, encoded: list) ->dict:
        decoded = dict()
        for data in encoded:
            formated_data = data.split(':')
            decoded[formated_data[0]] = formated_data[1]
        
        return decoded

    def call(self, parents, value, operation):
        rik = '/drv/content/properties'
        for parent in parents:
            rik+='/' + parent

        if operation == 'set':
            self._translations[rik] = value
            self.generate_object(parents, self._name, self._translations[rik])
        elif rik in self._translations:
            self.generate_object(parents, self._name, self._translations[rik])
        else:
            self._translations[rik] = ''
            self.generate_object(parents, self._name, self._translations[rik])
