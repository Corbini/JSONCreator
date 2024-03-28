from collections import OrderedDict
from copy import deepcopy
from source.model.value_formats import ValueFormats


class Operation:
    object_type = {}
    checker = ValueFormats()

    from source.model.oparation._add import add_end, add_before
    from source.model.oparation._duplicate import duplicate_end, duplicate_before
    from source.model.oparation._move import move_down, move_up
    from source.model.oparation._read import read
    from source.model.oparation._remove import remove
    from source.model.oparation._update import update

    def __init__(self, descriptor):
        self.descriptor = descriptor

    def input(self, parents, name, value, operation):
        parent = self._go_to_parent(parents)
        if parent is None:
            return

        match operation:
            case 'remove':
                self.remove(parents, name, value, parent)
            case 'read':
                self.read(parents, name, value, parent)
            case 'add':
                self.add_end(parents, name, value, parent)
            case 'add_before':
                self.add_before(parents, name, value, parent)
            case 'move_up':
                self.move_up(parents, name, value, parent)
            case 'move_down':
                self.move_down(parents, name, value, parent)
            case 'duplicate_before':
                self.duplicate_before(parents, name, value, parent)
            case 'duplicate_end':
                self.duplicate_end(parents, name, value, parent)
            case 'update':
                self.update(parents, name, value, parent)
            case _:
                print("Unsupported operation: ", operation)

    def _go_to_parent(self, parents):
        parent = self.descriptor.json['content']['properties']

        try:
            for object in parents[1:]:
                parent = parent[object]
        except:
            print("Incorrect parents")
            return None

        return parent

    def move_before(self, object, move_name, before_name):
        sort_list = list(object.keys())
        first = sort_list.index(before_name)

        sort_list = sort_list[first:]
        sort_list.pop(sort_list.index(move_name))

        for object_name in sort_list:
            object.move_to_end(object_name)

    def _duplicate(self, parents, name, data, parent):
        parent[name] = deepcopy(parent[data])
        self.descriptor.generate_object(parents, name, None)
        parents.append(name)
        self.descriptor.generate_tree(parent[name], parents)

    def _add(self, path, name, data='', parent=None) -> bool:
        if parent is None:
            parent = self.descriptor.json['content']['properties']
            for _parent in path:
                parent = parent[_parent]

        if data is None:
            parent[name] = OrderedDict()
            self.descriptor.generate_object(path, name, data)

            new_path = path + [name]
            # self.add_child(new_path, 'valueType', 'Branch', parent[name])

            model = Operation.object_type['Branch']
            for setting in model:
                self._add(new_path, setting, model[setting], parent[name])
        else:
            parent[name] = data
            self.descriptor.generate_object(list(path), name, data)

        return True

    def change_type(self, rel_path, object: OrderedDict, object_type):
        if object_type not in Operation.object_type:
            return

        if object_type == "Branch":
            children = list(object.keys())
            acceptable_settings = Operation.object_type[object_type]

            for child in children:
                if not isinstance(object[child], OrderedDict) and child not in acceptable_settings:
                    object.pop(child)
                    self.descriptor.remove_object(rel_path, child)

        else:
            data_keep = object_type == object['valueType']
            self.descriptor.validate_tree(object, Operation.object_type[object_type], rel_path, data_keep)
