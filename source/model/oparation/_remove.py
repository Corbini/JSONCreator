def remove(self, parents, name, data, parent):
    if name not in parent:
        return False

    self.descriptor.saves.save(self.descriptor.json)
    parent.pop(name)
    self.descriptor.remove_object(parents, name)
    return True