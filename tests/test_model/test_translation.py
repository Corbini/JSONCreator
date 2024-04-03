import unittest
from source.model.translation import Translation
from source import json_loader


class TestClass(unittest.TestCase):

    data = {
      "application": "golink",
      "type": "languageDefinition",
      "content": {
        "name": "English US",
        "translations": [
          "/drv/content/properties/device:Device",
          "/drv/content/properties/device/description:Detailed information on device",
          "/drv/content/properties/device/vendorName:Vendor name",
          "/drv/content/properties/device/vendorName/description:Vendor name"
        ]
      }
    }

    decoded = {
        '/drv/content/properties/device': 'Device',
        '/drv/content/properties/device/description': 'Detailed information on device',
        '/drv/content/properties/device/vendorName': 'Vendor name',
        '/drv/content/properties/device/vendorName/description': 'Vendor name',
    }

    def test_set_up(self):
        try:
            translation = Translation()
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

    def test_data_load(self):
        translation = Translation()

        try:
            translation.data_load('englishUs.json', self.data)
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

        self.assertEqual(translation._translations, self.decoded)
        self.assertEqual(translation._name, self.data['content']['name'])

    def test_properties(self):
        translation = Translation()
        translation.data_load('englishUs.json', self.data)

        self.assertEqual(translation.filepath, 'englishUs.json')
        self.assertEqual(translation.name, self.data['content']['name'])

    def test_create(self):
        translation = Translation()
        translation.create('englishUs.json', "English US")

        self.assertEqual(translation.filepath, 'englishUs.json')
        self.assertEqual(translation.name, self.data['content']['name'])

    def test_data_get(self):
        translation = Translation()
        translation.data_load('englishUs.json', self.data)

        self.assertEqual(translation.data_get(), self.data)

    def test_call(self):
        translation = Translation()
        translation.data_load('englishUs.json', self.data)

        translation.generate_object = lambda parents, name, value: True

        parents = ['a', 'b', 'c']

        try:
            translation.call(parents, 'new_value', 'set')
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

        self.assertEqual(translation._translations['/drv/content/properties/b/c'], 'new_value')

    calls = 0
    parents = []
    name = ''
    value = ''

    def observer(self, parents, name, value):
        self.calls += 1
        self.parents = parents
        self.name = name
        self.value = value

    def test_observer(self):
        translation = Translation()
        translation.data_load('englishUs.json', self.data)

        self.calls = 0
        translation.generate_object = lambda parents, name, value: self.observer(parents, name, value)

        parents_new = ['a', 'b', 'c']
        parents_existing = ['', 'device']

        translation.call(parents_new, 'test', 'get')
        self.assertEqual(self.calls, 1)
        self.assertEqual(self.parents, parents_new)
        self.assertEqual(self.name, 'English US')
        self.assertEqual(self.value, '')
        translation.call(parents_new, 'new_value', 'set')
        self.assertEqual(self.calls, 2)
        self.assertEqual(self.parents, parents_new)
        self.assertEqual(self.name, 'English US')
        self.assertEqual(self.value, 'new_value')
        translation.call(parents_new, 'new_value', 'get')
        self.assertEqual(self.calls, 3)
        self.assertEqual(self.parents, parents_new)
        self.assertEqual(self.name, 'English US')
        self.assertEqual(self.value, 'new_value')
        translation.call(parents_existing, 'new_value', 'get')
        self.assertEqual(self.calls, 4)
        self.assertEqual(self.parents, parents_existing)
        self.assertEqual(self.name, 'English US')
        self.assertEqual(self.value, 'Device')


