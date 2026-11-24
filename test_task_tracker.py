import tempfile
import unittest
from pathlib import Path
from task_tracker import add_task, complete_task, load_tasks, save_tasks


class TrackerTests(unittest.TestCase):
    def test_add_and_complete(self):
        tasks = []
        task = add_task(tasks, '  Revise Git  ', '2026-12-01')
        self.assertEqual(task['title'], 'Revise Git')
        self.assertFalse(task['done'])
        self.assertTrue(complete_task(tasks, task['id'])['done'])

    def test_ids_are_unique(self):
        tasks = []
        self.assertEqual(add_task(tasks, 'A')['id'], 1)
        self.assertEqual(add_task(tasks, 'B')['id'], 2)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            add_task([], '   ')
        with self.assertRaises(ValueError):
            add_task([], 'A', '2026-02-30')
        with self.assertRaises(ValueError):
            complete_task([], 99)

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'tasks.json'
            self.assertEqual(load_tasks(path), [])
            tasks = []
            add_task(tasks, 'Prepare lab')
            save_tasks(tasks, path)
            self.assertEqual(load_tasks(path), tasks)

    def test_corrupt_data_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'tasks.json'
            path.write_text('{broken', encoding='utf-8')
            with self.assertRaises(ValueError):
                load_tasks(path)
            self.assertEqual(path.read_text(), '{broken')

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'tasks.json'
            path.write_text('[{"id":1,"title":"A","done":false},'
                            '{"id":1,"title":"B","done":true}]')
            with self.assertRaises(ValueError):
                load_tasks(path)


if __name__ == '__main__':
    unittest.main()
