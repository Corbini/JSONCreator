from collections import OrderedDict


def _stringable_make_value_config(parameter: OrderedDict):
    # [maxBytes, maxChars, hidden]
    value_list = ['', '', '']

    if 'valueConfig' in parameter:
        value_list = parameter['valueConfig'].split('|')

    key_list = list(parameter.keys())
    for key in key_list:
        match key:
            case 'valueMaximum':
                value_list[1] = parameter[key]
                # object.pop(key)
            case 'valueType':
                if parameter[key] == "Password":
                    value_list[2] = "*"

    value_config = ""
    value_config += str(value_list[0])

    for value in value_list[1:]:
        value_config += '|'
        value_config += str(value)

    parameter['valueConfig'] = value_config


def _valueable_make_value_config(parameter: OrderedDict):
    # [valueMinimum, valueMaximum, valueScaler, if_float, scalar, valueUnit]
    value_list = ['', '', '', '', '', '']

    if 'valueConfig' in parameter:
        value_list = parameter['valueConfig'].split('|')

    key_list = list(parameter.keys())
    for key in key_list:
        match key:
            case 'valueMinimum':
                value_list[0] = parameter[key]
                parameter.pop(key)
            case 'valueMaximum':
                value_list[1] = parameter[key]
                parameter.pop(key)
            case 'valueUnit':
                value_list[5] = parameter[key]
                parameter.pop(key)

    value_config = ""
    value_config += str(value_list[0])

    for value in value_list[1:]:
        value_config += '|'
        value_config += str(value)

    parameter['valueConfig'] = value_config


def _object_make_valueConfig(parameter: OrderedDict):
    stringables = ['String', 'IP', 'IPv4', 'IPv6', 'SerialPort', 'UserName', 'Password']
    valueable = ['UInt8', 'UInt16', 'UInt32', 'Uint64', 'Int8', 'Int16', 'Int32', 'Int64', 'Real32', 'Real64']
    # [valueMinimum, valueMaximum, valueScaler, if_float, valueUnit]

    if parameter['valueType'] in stringables:
        _stringable_make_value_config(parameter)

    if parameter['valueType'] in valueable:
        _valueable_make_value_config(parameter)


def check_positions(object: OrderedDict):
    childs = list(object.keys())

    if len(childs) < 1:
        return False

    if childs[0] != "valueType":
        return False

    objects_begin = False
    for child in childs:
        if not objects_begin:
            if isinstance(object[child], OrderedDict):
                objects_begin = True
        else:
            if not isinstance(object[child], OrderedDict):
                return False

    return True


def sort_positions(object: OrderedDict):
    childs = list(object.keys())
    settings = []
    objects = []

    if "valueType" in childs:
        settings.append(["valueType", object.pop("valueType")])
        childs.remove("valueType")

    if "valueMaximum" in childs:
        settings.append(["valueMaximum", object.pop("valueMaximum")])
        childs.remove("valueMaximum")

    for child in childs:
        if isinstance(object[child], OrderedDict):
            objects.append([child, object.pop(child)])
        else:
            settings.append([child, object.pop(child)])

    for setting_structure in settings:
        object[setting_structure[0]] = setting_structure[1]

    for object_structure in objects:
        object[object_structure[0]] = object_structure[1]

            
def clean_json(parent):
    if check_positions(parent):
        sort_positions(parent)

    childs = list(parent.keys())

    rename_childs = {'maxValue': 'valueMaximum', 'minValue': 'valueMinimum', 'defaultValue': 'valueDefault',
                     'access': 'valueAccess', 'type': 'valueType', 'unit': 'valueUnit', 'lenght': 'valueMaximum'}
    # 'branch': 'Branch', 'string': 'String', 'dateTime': 'DataTime', 'boolean': 'Boolean', 'int16': "Int16"}
    incorrect_names = ['langEn', 'langPl']

    to_valueConfig = ['valueMinimum', 'valueMaximum', 'valueUnit']

    for child in childs:
        if isinstance(parent[child], OrderedDict):
            clean_json(parent[child])
        elif parent[child] == '':
            parent.pop(child)
        elif parent[child] == 'RW':
            parent.pop(child)
        elif child in rename_childs.keys():
            parent[rename_childs[child]] = parent.pop(child)
        elif child in incorrect_names:
            parent.pop(child)

    for child in childs:
        if child in to_valueConfig:
            _object_make_valueConfig(parent)
