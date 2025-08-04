# VS Code/Cursor Settings for Python

## Automatic Virtual Environment Activation

This project is configured so that VS Code and Cursor work seamlessly with the `.venv` virtual environment.

### What’s configured

1. **Automatic Python interpreter selection** – VS Code always uses `.venv/bin/python`
2. **Automatic terminal activation** – every new terminal automatically activates `.venv`

### How it works

- Open the project in Cursor/VS Code
- Restart Cursor if necessary
- Open a new terminal – it will automatically show `(.venv)` in the prompt
- Use `python` commands as usual – they will run inside the virtual environment

### Benefits

- ✅ No need to activate the environment manually
- ✅ No issues with Python aliases
- ✅ Settings are stored in git for the whole team
- ✅ Works with the debugger, tasks, and CI

### Configuration files

- `.vscode/settings.json` – interpreter settings
- `.venv/` – virtual environment (ignored by git)
