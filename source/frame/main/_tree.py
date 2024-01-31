from source.frame.parameter import Parameter


def tree_create(self, name):
    if self.parameter_tree is not None:
        self.parameter_tree.destroy()

    self.parameter_tree = Parameter(self.tree_frame, self.tree_frame, name)


def tree_update(self, parents, name, value=None):
    parent = self.parameter_tree
    while parents:
        parent_name = parents.pop(0)
        parent = parent.settings_list[parent_name]

    if value is None:
        parent.add_child(name)
    else:
        parent.update_setting(name, value)
