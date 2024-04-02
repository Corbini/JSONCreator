def duplicate_before(self, parents, name, data, parent) -> bool:
    new_name = data + '_duplicate'
    if new_name in parent:
        print("Object have: ", name)
        return False

    self.descriptor.saves.save(self.descriptor.json)
    self._duplicate(parents, new_name, data, parent)

    self.move_before(parent, new_name, data)

    updates_list = list(parent.keys())
    updates_list.remove('valueType')
    self.descriptor.reload_list(parents[:-1], parents[-1], updates_list)

    return True


def duplicate_end(self, parents, name, data, parent) -> bool:
    new_name = data + '_duplicate'
    if new_name in parent:
        print("Object have: ", name)
        return False

    self.descriptor.saves.save(self.descriptor.json)
    self._duplicate(parents, new_name, data, parent)

    return True
