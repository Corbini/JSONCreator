import unittest
from source.model.value_formats import ValueFormats


class TestClass(unittest.TestCase):
    object_type = \
        {
            "DataTime": {
                "valueType": "DataTime",
                "obis": "",
                "valueAccess": "",
                "valueInitial": ""
            }
        }

    def test_set_up(self):
        try:
            value_formats = ValueFormats()
            value_formats.object_type = self.object_type
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

    def test_is_is_obis(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_obis('0:0.0.0.0.0.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:-1.0.0.0.0.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.-1.0.0.0.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.-1.0.0.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.0.-1.0.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.0.0.-1.0;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.0.0.0.-1;0'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.0.0.0.0;-1'), False)
        self.assertEqual(value_formats._is_obis('1:0.0.0.0.0.0;0'), True)
        self.assertEqual(value_formats._is_obis('327767:255.255.255.255.255.255;255'), True)
        self.assertEqual(value_formats._is_obis('327768:255.255.255.255.255.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:256.255.255.255.255.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.256.255.255.255.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.255.25l6.255.255.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.255.255.256.255.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.255.255.255.256.255;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.255.255.255.255.256;255'), False)
        self.assertEqual(value_formats._is_obis('327767:255.255.255.255.255.255;256'), False)

    def test_is_rik(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_rik('-100'), False)
        self.assertEqual(value_formats._is_rik('rik'), True)
        self.assertEqual(value_formats._is_rik('/rik', True), True)
        self.assertEqual(value_formats._is_rik('rik/rik'), True)

    def test_is_rik_name(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_rik_name('-100'), False)
        self.assertEqual(value_formats._is_rik_name('100'), False)
        self.assertEqual(value_formats._is_rik_name('ri k'), False)
        self.assertEqual(value_formats._is_rik_name('Z'), False)
        self.assertEqual(value_formats._is_rik_name('Z12342'), False)
        self.assertEqual(value_formats._is_rik_name('rik'), True)
        self.assertEqual(value_formats._is_rik_name('z'), True)
        self.assertEqual(value_formats._is_rik_name('z1234'), True)

    def test_is_int_unlimited(self) -> bool:
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_int_unlimited('-100'), True)
        self.assertEqual(value_formats._is_int_unlimited('+100'), True)
        self.assertEqual(value_formats._is_int_unlimited('100'), True)
        self.assertEqual(value_formats._is_int_unlimited('asdf'), False)
        self.assertEqual(value_formats._is_int_unlimited(' 871243'), False)

    def test_is_int(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_int('-100', -100, 100), True)
        self.assertEqual(value_formats._is_int('+100', -100, 100), True)
        self.assertEqual(value_formats._is_int('100', -100, 100), True)
        self.assertEqual(value_formats._is_int('101', -100, 100), False)
        self.assertEqual(value_formats._is_int('-101', -100, 100), False)
        self.assertEqual(value_formats._is_int('-100', -99, 100), False)
        self.assertEqual(value_formats._is_int('+100', -100, 99), False)

    def test_is_config_stringable(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_config_stringable(['', '', ''], 2), False)
        self.assertEqual(value_formats._is_config_stringable(['', '', ''], 4), False)
        self.assertEqual(value_formats._is_config_stringable(['', '', ''], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['-1', '', ''], 3), False)
        self.assertEqual(value_formats._is_config_stringable(['0', '', ''], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['+0', '', ''], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '-1', ''], 3), False)
        self.assertEqual(value_formats._is_config_stringable(['', '0', ''], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '+0', ''], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '', 'false'], 3), False)
        self.assertEqual(value_formats._is_config_stringable(['', '', 'False'], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '', 'true'], 3), False)
        self.assertEqual(value_formats._is_config_stringable(['', '', 'True'], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '', '0'], 3), True)
        self.assertEqual(value_formats._is_config_stringable(['', '', '1'], 3), True)

    def test_is_config_valueable(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_config_valueable(['', '', '', '', '', ''], 5), False)
        self.assertEqual(value_formats._is_config_valueable(['', '', '', '', '', ''], 7), False)
        self.assertEqual(value_formats._is_config_valueable(['', '', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['gsfd', '', '', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['-100001', '', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['', 'dsfg', '', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['', '-100001', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['', '-100001', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '100', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '-100', '', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['12', '10', '', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '-100001', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '-100000', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', '', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100001', '', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', '-3', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', '-1', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', '-0', '', ''], 6), False)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', 'True', '', ''], 6), True)
        self.assertEqual(value_formats._is_config_valueable(['10', '12', '+100000', '1', '', ''], 6), True)

        # do more tests for other values?

    def test_is_config_tariff(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_config_tariff([''], 0), False)
        self.assertEqual(value_formats._is_config_tariff([''], 1), True)
        self.assertEqual(value_formats._is_config_tariff([''], 2), False)
        self.assertEqual(value_formats._is_config_tariff(['0'], 1), False)
        self.assertEqual(value_formats._is_config_tariff(['1'], 1), True)
        self.assertEqual(value_formats._is_config_tariff(['40'], 1), True)
        self.assertEqual(value_formats._is_config_tariff(['+41'], 1), False)

    def test_is_config_multichoice(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'option1'], 2), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'option1'], 3), True)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'option1'], 4), False)
        self.assertEqual(value_formats._is_config_multichoice(['0', '', 'option1'], 1), False)
        self.assertEqual(value_formats._is_config_multichoice(['1', '', 'option1'], 3), True)
        self.assertEqual(value_formats._is_config_multichoice(['40', '', 'option1'], 3), True)
        self.assertEqual(value_formats._is_config_multichoice(['+41', '', 'option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['40', '1', 'option1'], 3), True)
        self.assertEqual(value_formats._is_config_multichoice(['40', 'c', 'option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'option1'], 3), True)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', '1option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', ' option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', '-option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'arr/option1'], 3), True)

    def test_is_config(self):
        value_formats = ValueFormats()
        value_formats.object_type = self.object_type

        self.assertEqual(value_formats._is_config_multichoice(['5', '', '-option1'], 3), False)
        self.assertEqual(value_formats._is_config_multichoice(['5', '', 'arr/option1'], 3), True)


