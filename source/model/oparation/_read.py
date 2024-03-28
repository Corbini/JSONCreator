def read(self, parents, name, data, parent):
    if name not in parent:
        self.descriptor.generate_object(parents, name, '')
        return False

    self.descriptor.generate_object(parents, name, parent[name])

    return True