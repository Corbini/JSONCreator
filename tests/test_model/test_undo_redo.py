import unittest
from source.model.undo_redo import UndoRedo


class TestClass(unittest.TestCase):
    def test_set_up(self):
        try:
            undo_redo = UndoRedo(8)
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

    def test_save(self):
        undo_redo = UndoRedo(4)

        data = {'abc': 0}

        try:
            undo_redo.save(data)
        except Exception as e:
            self.fail('Class cannot by initialised. Raised: ' + str(e))

        self.assertEqual(data == undo_redo._saves[0], True)
        data['bcd'] = 'dziad'
        self.assertEqual(data == undo_redo._saves[0], False)

    def test_reload(self):
        undo_redo = UndoRedo(4)

        data = {'abc': 0}
        undo_redo.save(data)
        self.assertEqual(data == undo_redo.reload(), True)
        data2 = {'abc': 1}
        undo_redo.save(data2)
        self.assertEqual(data2 == undo_redo.reload(), True)

    def test_save(self):
        undo_redo = UndoRedo(4)

        data = {'abc': 0}
        undo_redo.save(data)
        self.assertEqual(data == undo_redo.undo(), True)
        data2 = {'abc': 1}
        undo_redo.save(data2)
        self.assertEqual(data == undo_redo.undo(), False)

        data3 = {'bcd': 2}
        undo_redo.save(data3)
        data4 = {'cde': 3}
        undo_redo.save(data4)
        self.assertEqual(data3 == undo_redo.undo(), True)

    def test_redo(self):
        undo_redo = UndoRedo(4)

        data = {'abc': 0}
        data2 = {'abc': 1}
        data3 = {'bcd': 2}
        data4 = {'cde': 3}
        data5 = {'cde': 4}

        undo_redo.save(data)
        undo_redo.save(data2)
        undo_redo.save(data3)
        undo_redo.save(data4)

        undo_redo.undo()
        undo_redo.undo()

        self.assertEqual(data3 == undo_redo.redo(), True)

        undo_redo.save(data5)

        undo_redo.undo()
        self.assertEqual(data5 == undo_redo.redo(), True)

        undo_redo.undo()
        undo_redo.undo()

        undo_redo.save(data5)

        undo_redo.undo()
        self.assertEqual(data5 == undo_redo.redo(), True)
