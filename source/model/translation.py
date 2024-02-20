import json

class Translation:
    generate_object = lambda self, parents, name, data: print(parents, name, data)

    def __init__(self):
        self._filepath = ''

        self._name = ''
        self._translations = dict()

    @property
    def name(self):
        return self._name
    
    @property
    def filepath(self):
        return self._filepath

    def create(self, filename, name):
        self._name = name
        self._translations = dict()

        print('Program wants to create ', name, ' language in file: ', filename)

    def data_load(self, filepath, json_data) -> bool:
        self._filepath = filepath

        self._name = json_data['content']['name']
        encoded = json_data['content']['translations']
        self._translations = self._decode(encoded)
        return True

    def data_get(self) -> json:
        encoded = self._encode()
        content = {'name': self._name, 'translations': encoded}
        data = {'application': 'golink', 'type': 'languageDefinition'}
        data['content'] = content
        return data

    def _encode(self) -> list:
        encoded = list()

        for key in self._translations.keys():
            line = key + ':'
            line += self._translations[key]
            encoded.append(line)

        return encoded
    
    def _decode(self, encoded: list) ->dict:
        decoded = dict()
        for data in encoded:
            formated_data = data.split(':', 1)
            decoded[formated_data[0]] = formated_data[1]
        
        return decoded

    def call(self, parents, value, operation):
        
        if len(parents) > 1:
            rik = '/drv/content/properties'
            for parent in parents[1:]:
                rik+='/' + parent
        else:
            rik = parents[0]

        if operation == 'set':
            self._translations[rik] = value
            self.generate_object(parents, self._name, self._translations[rik])
        elif rik in self._translations:
            self.generate_object(parents, self._name, self._translations[rik])
        else:
            self.generate_object(parents, self._name, '')
