from source.frame.parameter import Parameter


def tree_create(self, name):
    if self.parameter_tree is not None:
        self.parameter_tree.destroy()

    self.parameter_tree = Parameter(None, self.device.frame, name)
    self.parameter_tree.translations.reload_language()


def tree_update(self, parents, name, value=None):
    parent = self.parameter_tree
    parents.pop(0)
    while len(parents):
        if parents[0] in parent.child.list:
            parent = parent.child.list[parents.pop(0)]
        else:
            break

    if value is None:
        parent.add_child(name)
    else:
        if len(parents):
            parent.update_setting(name, parents + [value])
        else:
            parent.update_setting(name, value)


def tree_data_error(self, parents, name, value):
    parent = self.parameter_tree
    for _parent in parents[1:]:
        parent = parent.child.list[_parent]

    parent.warn(name, value)


def tree_remove(self, parents, name):
    parent = self.parameter_tree
    for _parent in parents[1:]:
        parent = parent.child.list[_parent]

    parent.child.remove(name)


def tree_reload_list(self, parents, name, list):

    parent = self.parameter_tree
    if len(parents) > 1:
        for _parent in parents[1:]:
            parent = parent.child.list[_parent]

    parent.child.refresh_list(list)
