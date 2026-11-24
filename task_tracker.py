"""A small offline task tracker for the UCS 745 Git lab."""
import argparse
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name('tasks.json')


def get_heading():
    """Both Git feature branches will deliberately edit this line."""
    return 'Student Task Tracker'


def load_tasks(path=DATA_FILE):
    if not path.exists():
        return []
    tasks = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(tasks, list):
        raise ValueError('Task data must be a list.')
    ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError('Invalid task record.')
        if (type(task.get('id')) is not int or task['id'] <= 0
                or task['id'] in ids or not isinstance(task.get('title'), str)
                or not task['title'].strip() or type(task.get('done')) is not bool):
            raise ValueError('Invalid or duplicate task record.')
        if task.get('due') is not None:
            date.fromisoformat(task['due'])
        ids.add(task['id'])
    return tasks


def save_tasks(tasks, path=DATA_FILE):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(tasks, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def add_task(tasks, title, due=None):
    title = title.strip()
    if not title:
        raise ValueError('Task title cannot be empty.')
    if due:
        due = date.fromisoformat(due).isoformat()
    task = {'id': max((t['id'] for t in tasks), default=0) + 1,
            'title': title, 'due': due, 'done': False}
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            return task
    raise ValueError(f'Task {task_id} does not exist.')


def main():
    parser = argparse.ArgumentParser(description=get_heading())
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add', help='Add a task')
    add.add_argument('title')
    add.add_argument('--due', help='Optional due date: YYYY-MM-DD')
    listing = commands.add_parser('list', help='Show saved tasks')
    listing.add_argument('--pending', action='store_true')
    done = commands.add_parser('done', help='Mark a task complete')
    done.add_argument('id', type=int)
    args = parser.parse_args()
    try:
        tasks = load_tasks()
        print(get_heading())
        if args.command == 'add':
            task = add_task(tasks, args.title, args.due)
            save_tasks(tasks)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == 'done':
            task = complete_task(tasks, args.id)
            save_tasks(tasks)
            print(f"Completed task {task['id']}: {task['title']}")
        else:
            visible = [t for t in tasks if not (args.pending and t['done'])]
            if not visible:
                print('No matching tasks.')
            for task in visible:
                status = 'DONE' if task['done'] else 'TODO'
                due = task.get('due') or 'none'
                print(f"{task['id']:>3} [{status}] {task['title']} | Due: {due}")
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
