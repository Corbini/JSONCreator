
class ValueFormats:
    object_type = {}

    stringables = ['String', 'IP', 'IPv4', 'IPv6', 'SerialPort', 'UserName', 'Password']
    valueable = ['UInt8', 'UInt16', 'UInt32', 'Uint64', 'Int8', 'Int16', 'Int32', 'Int64', 'Real32', 'Real64', 'Numeric']

    call_error = lambda parents, name, text: print(parents, name, text)

    error = ''

    def __init__(self, object_type):
        self._types = []
        # self._checks[format_name](value)

    def _is_setting_name(self, name) -> bool:
        if name not in self._types:
            self.error = 'TYPE: ' + name + 'is not a type'
            return False

        return True

    def _is_rik(self, value) -> bool:
        if len(value) == 0:
            self.error = 'RIk: ' + value + 'is empty'
            return False

        if not value[0].islower():
            self.error = 'RIK: ' + value + ' dont have a lower first character'
            return False

        allowed = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

        for character in value:
            if character not in allowed:
                self.error = 'RIK: ' + value + 'is not allowed in RIK'
                return False

        return True

    def _is_int(self, value) -> bool:
        if value[0] in ('-', '+'):
            value[1:].isdigit()
        return value.isdigit()

    def _is_config(self, value: str, object_type: str) -> bool:
        if not isinstance(value, str):
            self.error = 'Config: ' + value + 'is not string'
            return False

        config_list = value.split('|')

        size = len(config_list)
        if object_type in self.stringables:
            return self._is_config_stringable(config_list, size)

        elif object_type in self.valueable:
            return self._is_config_valueable(config_list, size)

        else:
            match object_type:
                case 'Tariff':
                    return self._is_config_tariff(config_list, size)

                case 'MultiChoice':
                    return self._is_config_multichoice(config_list, size)

                case _:
                    return True

    def _is_config_stringable(self, config_list, size) -> bool:
        if size != 3:
            self.error = 'Config: ' + config_list + 'is not a list of 3'
            return False

        return (
            (self._is_int(config_list[0], 0, 100000) or config_list[0] == '')
            and (self._is_int(config_list[1], 0, 100000) or config_list[1] == '')
            and (self._is_bool(config_list[2]) or config_list[2] == '')
        )

    def _is_config_valueable(self, config_list, size) -> bool:
        if size != 6:
            self.error = 'Config: ' + config_list + 'is not a list of 6'
            return False

        return (self._is_int(config_list[0], -100000, 100000) and
                self._is_int(config_list[1], -100000, 100000) and
                self._is_int(config_list[2], -100000, 100000) and
                self._is_bool(config_list[3]))

    def _is_value_access(self, value):
        if value in ['W', 'R', 'A', 'N']:
            return True

        self.error = ''

        return False

    def _is_config_tariff(self, config_list, size) -> bool:
        if size != 1:
            self.error = 'Config: ' + config_list + ' is not a list of 1'
            return False

        return self._is_int(config_list[0], 0, 100000)

    def _is_config_multichoice(self, config_list, size) -> bool:
        if size != 3:
            self.error = 'Config: ' + config_list + ' is not a list of 3'
            return False

        if not self._is_int(config_list[0], 0, 100000):
            return False

        if not self._is_bool(config_list[1]):
            return False

        options = config_list[1].split(';')

        if len(options) < 1:
            self.error = 'Config: ' + config_list + ' incorect format'
            return False

        for option in options:
            if self._is_rik(option):
                return False

        return True

    def _is_obis(self, value):
        seperated_class = value.split(':')
        if len(seperated_class) != 2:
            self.error = 'Obis: ' + value + ' incorrect amount of class'
            return False
        if self._is_int(seperated_class[0], 0, 255) is False:
            return False

        seperated_atribute = seperated_class[1].split(';')
        if len(seperated_atribute) != 2:
            self.error = 'Obis: ' + value + ' incorrect amount of class'
            return False
        if self._is_int(seperated_atribute[1], 0, 255) is False:
            return False

        obis = seperated_atribute[0].split('.')

        if len(obis) != 6:
            self.error = 'Obis: ' + value + ' incorrect amount of obis int'
            return False
        for number in obis:
            if self._is_int(number, 0, 255) is False:
                return False

        return True

    def _is_int(self, value, minimum, maximum) -> bool:
        if value == '':
            return True

        is_digit = False
        if value[0] in ('-', '+'):
            is_digit = value[1:].isdigit()
        else:
            is_digit = value.isdigit()

        if not is_digit:
            return False

        if not minimum <= int(value) <= maximum:
            self.error = 'Int: ' + value + ' not between ' + minimum + ' and ' + maximum
            return False

        return True

    def _is_bool(self, value) -> bool:
        if not (value == 'True' or value == 'False' or value == '1' or value == '0' or value == ''):
            self.error = 'Bool: ' + value + ' incorrect format'
            return False
        return True

    def _check(self, parent_type, name, data):
        print(parent_type, name, data)

        match name:
            case 'valueType':
                if data in ValueFormats.object_type:
                    return True

                self.error = False
                return False
            case 'enumKey':
                return True
            case 'valueAccess':
                return self._is_value_access(data)
            case 'valueMaximum':
                return self._is_int(data, 0, 100000)
            case 'obis':
                return self._is_obis(data)
            case 'valueConfig':
                return self._is_config(data, parent_type)
            case _:
                return self._is_rik(data)

    def check(self, parents, parent_type, name, data):
        if not self._check(parent_type, name, data):
            result = list()
            ValueFormats.call_error(parents, name, self.error)
            return False

        return True
