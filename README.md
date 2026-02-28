# Task Tracker CLI

**Repository:** [github.com/amythp138/Task-Tracker-CLI](https://github.com/amythp138/Task-Tracker-CLI)  
**Project:** [roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)

A simple command-line task tracker. Add, update, delete, and list tasks with statuses (todo, in progress, done). Tasks are stored in a local `tasks.json` file.

## Features

- **Add** tasks with a description
- **Update** task descriptions
- **Delete** tasks
- **Mark** tasks as in progress or done
- **List** all tasks or filter by status (all, in progress, done, todo)
- **Interactive mode** — menu-driven prompts for all actions
- **CLI mode** — run single commands from the terminal

## Requirements

- Python 3.6+

No extra packages; uses only the standard library.

## Quick Start

```bash
# Interactive mode (menu + prompts)
python task_tracker.py

# Or use commands directly
python task_tracker.py add "Finish the report"
python task_tracker.py list
```

## Usage

### Interactive mode

Run with no arguments to get a numbered menu and follow the prompts:

```bash
python task_tracker.py
```

You’ll be asked to choose an action (add, list, update, delete, mark in progress, mark done, quit) and to enter any required info (e.g. description, task ID). When you list tasks, full task IDs are shown so you can copy-paste them for update, delete, or mark.

### Command-line commands

| Command | Description |
|--------|-------------|
| `add [description]` | Add a task. If description is omitted, you’re prompted for it. |
| `list [--status STATUS]` | List tasks. Optional: `--status todo`, `in-progress`, or `done`. |
| `update TASK_ID DESCRIPTION` | Update a task’s description. |
| `delete TASK_ID` | Delete a task. |
| `in-progress TASK_ID` | Mark a task as in progress. |
| `done TASK_ID` | Mark a task as done. |

**Examples**

```bash
python task_tracker.py add "Buy groceries"
python task_tracker.py list
python task_tracker.py list --status done
python task_tracker.py update b07eb35a-6cb0-4a3f-94e2-e938805ca7eb "Updated description"
python task_tracker.py done b07eb35a-6cb0-4a3f-94e2-e938805ca7eb
python task_tracker.py delete b07eb35a-6cb0-4a3f-94e2-e938805ca7eb
```

Use `python task_tracker.py --help` and `python task_tracker.py <command> --help` for more options.

## Data storage

Tasks are saved in `tasks.json` in the same directory as the script. Each task has:

- **id** — UUID
- **description** — Task text
- **status** — `TODO`, `INPROGRESS`, or `DONE`
- **created_at** — ISO timestamp
- **updated_at** — ISO timestamp

You can edit or backup this file if needed.

## License

Use and modify as you like.
