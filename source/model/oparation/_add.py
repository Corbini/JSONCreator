def add_end(self, parents, name, data, parent) -> bool:
    if name in parent:
        print("Object have: ", name)
        return False

    self.descriptor.saves.save(self.descriptor.json)
    return self._add(parents, name, data, parent)


def add_before(self, parents, name, data, parent) -> bool:
    if name in parent:
        print("Object have: ", name)
        return False

    self.descriptor.saves.save(self.descriptor.json)
    self._add(parents, name, data, parent)
    self.descriptor.generate_object(parents, name, data)

    self.move_before(parent, name, data)

    updates_list = list(parent.keys())
    updates_list.remove('valueType')
    self.descriptor.reload_list(parents[:-1], parents[-1], updates_list)

    return True
