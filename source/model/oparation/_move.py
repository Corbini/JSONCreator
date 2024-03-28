def move_down(self, parents, name, data, parent) -> bool:
    self.descriptor.saves.save(self.descriptor.json)
    sort_list = list(parent.keys())
    before = sort_list.index(name) + 1
    if before < 0:
        return False

    self.move_before(parent, sort_list[before], name)

    updates_list = list(parent.keys())
    updates_list.remove('valueType')
    self.descriptor.reload_list(parents, name, updates_list)

    return True

def move_up(self, parents, name, data, parent) -> bool:
    self.descriptor.saves.save(self.descriptor.json)
    sort_list = list(parent.keys())
    before = sort_list.index(name) - 1
    if before < 0:
        return False

    self.move_before(parent, name, sort_list[before])

    updates_list = list(parent.keys())
    updates_list.remove('valueType')
    self.descriptor.reload_list(parents, name, updates_list)

    return True