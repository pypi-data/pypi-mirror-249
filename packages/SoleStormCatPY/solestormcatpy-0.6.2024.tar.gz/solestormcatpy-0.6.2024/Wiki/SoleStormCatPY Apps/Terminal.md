# Terminal
"terminal" is a way to easily access the user's system default terminal. So, if you want to check for an update for your package, you could easily do that! There are also two versions of "terminal": "terminal" and "terminalGUI". Here is how you can tell which each is!

## Both "Terminal" Types
There are two types of "terminal" Here they are:
"terminal":
This is the default terminal runner. Everything is done within the terminal.

"terminalGUI":
This asks the user for a command within a `tkinter` GUI. The output will be printed in the real terminal. (Requires `tkinter` module)

## How To Use
To run "terminal" in your application, here is a way to use it. As per the example above, updating your package would require the `command` string, which holds your command that you are going to run (example: `command = 'pip install tkinter'`), along with `SoleStormCatPY.terminal.terminalrun(command)` (For "terminal), or run `import SoleStormCatPY.terminal.terminalGUI()` (For "terminalGUI", does NOT require `command`).
Have Fun Running commands via Python!
