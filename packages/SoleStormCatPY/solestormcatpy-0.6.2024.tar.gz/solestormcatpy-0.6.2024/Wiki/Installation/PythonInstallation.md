# Python Installation
(All Installation Steps were provided by the Python Software Foundation)

To install Python, one must go to [Python's Download Folder](https://python.org/downloads), where you can access Python's downloads. To find more information for your system, look below:

## Windows
Windows is the system that takes the most effort to install. There are many installers for Python, but for this installer, we'll be using what is called the Full Installer. The Full Installer does as it says, as it lets you download nearly everything that Python offers. Here is what you need to do to download Python on your Windows PC:

1. Navigate to [Python's Windows Download Folder](https://python.org/downloads/windows), where you can find the "Latest Python 3 Release - Python 3.x.y" (where x and y are any number) link, under the section "Python Releases For Windows." Click that link.
1. Scroll down to the "Files" section, where you'll find multiple downloads for multiple systems. Find the two `.msi` files, and download the one that matches your system (likely 64-bit.)
1. Open the installer, where you'll be guided with two different installation options, "Install Now" or "Customize Installation." If you click "Install Now," Python will automatically install to your system (UAC may be required.) If you want to customize installation, click "Customize Installation," and follow the steps under "Customize Installation" section. If you want, you may click the checkbox that says "Add python.exe to PATH."

### Customize Installation
You have choosen to customize your installation. The first screen that you'll be greeted with will have the following options:

1. Documentation: Documentation allows you to get help (even when offline) with pre-installed Python Modules and Python itself
1. pip: Pip is an installer that allows you to install third-party packages, such as SoleStormCatPY
1. tk: Tkinter (tk) is a module that allows for a person to create a GUI application, and modules such as SoleStormCatPY’s GUI counterpart requires Tkinter to be on the system. IDLE is an Python script editing service that runs on tkinter.
1. Python Test Suite: The Python Test Suite allows a person to test their scripts
1. py launcher: The Python Launcher helps with launching Python

As you click `Next`, here are the following options you get:

1. Install Python 3.x for all users: This lets an administrator download Python for all users on the system
1. Associating files with Python: This associates files with Python better
1. Create shortcuts for installed applications: This creates shortcuts for Python, the Python Launcher (if you installed it), and IDLE (If you installed it)
1. Adding Python to environmental variables: This allows for a better experiance with Python
1. Precompiling standard libary: This allows Python to compile the standard libraries before opening Python for the first time
1. Debugging symbols and binaries: These are for more advanced users, and the latter requires Microsoft's Visual Studio version 2017 or newer.
1. Customize install location: This customizes where Python is installed. It is best to stay with Python's default location.

When you click `Install`, Python will be installed to your system (May require UAC authorization.)

## MacOS
As a default, MacOS should already have Python installed, as Apple uses Python to help run their system.

## Linux
As a default, most Linux Distibutions should already have Python installed, but if it isn't, here are commands that you can run on your system (based on distribution):

### Ubuntu and Debian
You may run the command `sudo apt-get install python3 python3-dev` in your terminal, but you'll require root access (`sudo`) to access this command.

### Arch Linux
You may run the command `pacman -S python3` in your terminal to install Python onto your system.

### Fedora
You may run the command `dnf install python3 python3-devel` in your terminal to install Python onto your system.

