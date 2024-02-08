import json

class Translation:
    
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

    def data_load(self, json_data) -> bool:

        self._name = json_data['content']['name']
        encoded = json_data['content']['translations']
        self._translations = self._decode(encoded)
        return True

    def data_get(self, filename) -> json:
        encoded = self._encode()

        return json({'application': 'golink', 'type': 'languageDefinition', 'content': {'name': self._name, 'translations': encoded}})

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
