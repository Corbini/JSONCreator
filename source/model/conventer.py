from collections import OrderedDict


def _object_make_valueConfig(object: OrderedDict):
    # [valueMinimum, valueMaximum, valueScaler, if_float, valueUnit]
    value_list = ['','','','','']
    
    if 'valueConfig' in object:
        value_list = object['valueConfig'].split('|')


    key_list = list(object.keys())
    for key in key_list:
        match key:
            case 'valueMinimum':
                value_list[0] = object[key]
                object.pop(key)
            case 'valueMaximum':
                value_list[1] = object[key]
                # object.pop(key)
            case 'valueUnit':
                value_list[4] = object[key]
                object.pop(key)

    value_config = ""
    value_config += str(value_list[0])

    for value in value_list[1:]:
        value_config += '|'
        value_config += str(value)

    object['valueConfig'] = value_config

            
def clean_json(parent):
    childs = list(parent.keys())

    rename_childs = {'maxValue': 'valueMaximum', 'minValue': 'valueMinimum', 'defaultValue': 'valueDefault', 'access': 'valueAccess', 'type': 'valueType', 'unit': 'valueUnit', 'lenght': 'valueMaximum'}
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
