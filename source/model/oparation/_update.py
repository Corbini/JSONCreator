from collections import OrderedDict
from copy import deepcopy


def _reset_correct_data(self, parents, name, parent):
        if name in parent:
            if isinstance(parent[name], OrderedDict):
                parents.append(name)
                self.generate_object(parents, 'name', name)
            else:
                self.generate_object(parents, name, parent[name])
        else:
            self.generate_object(parents, name, '')


def update(self, parents, name, data, parent) -> bool:
    self.descriptor.saves.save(self.descriptor.json)
    # Checks if value is correct
    if not self.checker.check(parents, parent['valueType'], name, data):
        # _reset_correct_data(self, parents, name, parent)
        return False

    if name not in parent:
        return self.add_end(parents, name, data, parent)

    if isinstance(parent[name], OrderedDict):
        # Rename object
        if name == data:
            return False

        if data in parent:
            return False

        keys = list(parent.keys())
        keys[keys.index(name)] = data
        parent[data] = parent.pop(name)

        flag = False
        for key in keys:
            if flag:
                parent.move_to_end(key)
            elif key == data:
                flag = True

        parents.append(name)
        name = 'name'
    else:
        parent[name] = deepcopy(data)
        if name == 'valueType':
            self.change_type(parents, parent, data)

    self.descriptor.generate_object(parents, name, data)
    return True
