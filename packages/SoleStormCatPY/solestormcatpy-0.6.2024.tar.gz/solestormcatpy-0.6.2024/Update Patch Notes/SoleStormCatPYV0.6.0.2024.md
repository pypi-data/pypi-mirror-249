# SoleStormCatPY V0.6.2024
This was an update released by SoleStormCat Corp on January 1, 2024    
To install, run `python3 -m pip install SoleStormCatPY==0.6.2024` (MacOS and Linux) or `py -m pip install SoleStormCatPY==0.6.2024` (Windows)

## Update Info
Version: 0.6.2024     
Author: SoleStormCat Corp     
Released On: [GitHub](https://github.com/solestormcat-corp/solestormcatpy) and [PyPi](https://pypi.org/project/SoleStormCatPY/0.6.2024/)     
Release Date: January 1, 2024 (1/1/2024)     
Offical Update Name: SoleStormCatPY New Years 2024

## Patch Notes

### Features
1. Updated LICENSE file (Lines 1-3)
1. Introduced unixtimecon, which allows for user to convert unix time to local time and vice versa, along with printing the current unix time. (33 Lines)
1. Added unixTime module (SoleStormCat-Made based from SoleStormCatPY unixtimecon.py) to interactiveShell, which runs SoleStormCatPY's unixtimecon.(Lines 86-100, Line 25)
1. Added efile module (SoleStormCat-Made) to interactiveShell, which allows for a user to open Notepad (Windows) or nano (Linux and MacOS). (Line 24, Lines 78-83)
1. Added quit, exit, and stop modules to interactiveShell, which closses interactiveShell and SoleStormCatPY. (Line 23, Lines 72-77)
1. Added "Update Patch Notes" folder to GitHub, which allows for a person to track patch notes (starting from version 0.6.2024).
1. Added unixTime (unixtimecon) to sscPyStandalone CMD menu. (Lines 220-222, Line 241)
1. Added interactiveShell to sscPyStandalone GUI menu (was already in CMD menu) (Lines 37-55, Line 95, Lines 123-124)
1. Added a SoleStormCatPY Upgrade option to interactiveShell. (Lines 41-47, Line 51)
1. Added killpc module (SoleStormCat-Made) to interactiveShell, which shuts down the computer. (Lines 105-111 and Lines 121-122)
1. Added restartpc module (SoleStormCat-Made) to interactiveShell, which reboots the computer. (Lines 112-120)
1. Added SECURITY.md, which outlines how to report a security issue.
1. Updated SoleStormCatPY.ico (SoleStormCatPY/src/SoleStormCatPY/SoleStormCatPY.ico) to match SoleStormCat Corporation's new logos.
1. Added a basic Wiki (SoleStormCatPY/Wiki). You may see the added Wiki pages at section "Wiki Pages"
1. Updated README.md to migrate module information to the Wiki
1. Added an installation folder for older versions (SoleStormCatPY/Releases/Python/Old pip Installers)


### Bugs fixed
1. The update button in sscPyStandalone should work now, line 73 (or line 54 in V0.5.7) was changed from 'UpgradeLabel.mainloop()' to 'UpgradeFrame.mainloop()' (No GitHub issue was marked to this issue)

### Wiki Pages
1. Added a Python installation Guide to Wiki (SoleStormCatPY/Wiki/Installation/PythonInstallation.md)
1. Added a SoleStormCatPY instllation Guide to Wiki (SoleStormCatPY/Wiki/Installation/SoleStormCatPYInstallation.md)
1. Added MathSolver to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/MathSolver.md)
1. Added WebOpen to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/WebOpen.md)
1. Added Terminal to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/Terminal.md)
1. Added SystemInfo to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/SystemInfo.md)
1. Added ClockTimer to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/ClockTimer.md)
1. Added Files to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/Files.md)
1. Added GreeNotes to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/GreeNotes.md)
1. Added appOpener to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/appOpener.md)
1. Added interactiveShell to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/interactiveShell.py)
1. Added UnixTimeConvertor to Wiki (SoleStormCatPY/Wiki/SoleStormCatPY Apps/UnixTimeConvertor.md)