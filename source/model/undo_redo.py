from copy import deepcopy


class UndoRedo:
    def __init__(self, maximum):

        self._maximum = maximum
        self._saves = []
        self._position = -1

    def save(self, data):
        saved_data = deepcopy(data)
        if self._position >= self._maximum:
            self._saves.pop(0)
        else:
            self._position += 1
            self._saves = self._saves[:self._position]

        self._saves.insert(self._position, saved_data)

    def reload(self):
        return self._saves[self._position]

    def undo(self):
        if self._position < 0:
            return None

        self._position -= 1

        return self._saves[self._position]

    def redo(self):
        if self._position >= len(self._saves) - 1:
            return None

        self._position += 1

        return self._saves[self._position]
