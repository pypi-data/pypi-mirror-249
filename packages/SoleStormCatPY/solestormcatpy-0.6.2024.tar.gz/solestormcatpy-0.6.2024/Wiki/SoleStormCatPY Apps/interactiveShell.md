# Interactive Shell
The Interactive Shell is an intercative terminal developed by SoleStormCat Corp. It holds custom commands, along with being able to use system commands!

## How to Use
There are two ways to open the interactive shell. The first being a blank shell, and the second opening the shell with a command.
To open a blank shell, use `SoleStormCatPY.interactiveShell.shellOpen()`. To open a command shell, use `SoleStormCatPY.interactiveShell.shellUse('command')`.

## Currently Supported commands
The commands that are custom made are below:

### help
`help` is a command that shows all the active commands that are made by SoleStormCat. 
To find system commands, run `help --os`. 
To find help for specific modules, run `help -m name` (with name being the module name.)

### sscpy
`sscpy` is the opener for SoleStormCatPY. To open SoleStormCatPY in GUI, run `sscpy --gui`.
To update SoleStormCatPY, run `sscpy --upgrade`

### python
`python` is a coding platform developed by the Python Software Foundation.

### web
`web` utilizes the SoleStormCatPY `webOpen` module to use a web browser.
You can run `web --tk` to use a `tkinter` window for the URL asker.
You can run `web --df` to use your defult browser.

### quit and exit and stop
These describe themseves.

### efile
`efile` opens a text editor. For Windows, Notepad is opened, but for Linux and MacOS, nano is opened.

### unixTime
`unixTime` runs SoleStormCatPY's `unixtimecon` module, and in this case shows the current Unix time and allows for a person to see what a specific Unix time is in their area.
You can run `unixTime --time` if you just want to see the current Unix time.
You can run `unixTime --convertor` if you just want to use the convertor.

### killpc
`killpc` shuts down a PC.

### restartpc
`restartpc` reboots a PC.
