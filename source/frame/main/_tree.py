from source.frame.parameter import Parameter


def tree_create(self, name):
    if self.parameter_tree is not None:
        self.parameter_tree.destroy()

    self.parameter_tree = Parameter(None, self.tree_frame, name)
    self.parameter_tree.update_languages()


def tree_update(self, parents, name, value=None):
    parent = self.parameter_tree
    for _parent in parents:
        parent = parent.child.list[_parent]

    if value is None:
        parent.add_child(name)
    else:
        parent.update_setting(name, value)

def tree_remove(self, parents, name):
    parent = self.parameter_tree
    for _parent in parents:
        parent = parent.child.list[_parent]

    parent.remove_child(name)
