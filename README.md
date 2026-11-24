# Student Task Tracker

Lab project prepared for Brahmjeet Singh, group 4Q16, roll number 102317163.
A single-user Python command-line application that saves student tasks locally.

## Requirements
Python 3.9 or newer. No external packages.

## Run
```sh
python3 task_tracker.py add "Revise Git branching" --due 2026-12-01
python3 task_tracker.py add "Prepare Linux lab"
python3 task_tracker.py list
python3 task_tracker.py done 1
python3 task_tracker.py list --pending
python3 -m unittest -v
```
Use `python` instead of `python3` if that is your Python command.
Dates above are sample data, not an assignment deadline.

## Files
- `task_tracker.py`: command parsing, validation, task operations and JSON storage.
- `test_task_tracker.py`: tests of behavior and persistence.
- `tasks.json`: generated local data, excluded from Git.

## Scope and limitations
One user and one running writer at a time. No accounts, cloud sync, notifications,
editing or deletion. The temporary-file replacement reduces incomplete writes;
it does not provide concurrency control. Dates do not trigger reminders.
Malformed data produces an error rather than silently resetting saved tasks.

## Git lab
The `get_heading()` return line is the intentional conflict location.
Follow the separate Git walkthrough to edit it differently in two independent
branches, merge them, inspect the conflict and resolve it manually.
The starter contains no manufactured Git history or practical screenshots.
