#This allows for a user to run their terminal inside of a SoleStormCat-made Interactive Shell! Inside are some commands that are custom made by SoleStormCat, and can also run your normal commands!
#How to use:
#import SoleStormCatPY.interactiveShell as cmd
#cmd.shellOpen()

#You may also open the shell using some code by using:
#cmd.shellUse('command')

import os
import platform as pf

username = os.getlogin()
hostname = pf.node()

def shellUse(command):
    print('')
    if command == 'help':
        print('Here are the active SoleStormCat Commands:')
        print('help')
        print('sscpy')
        print('python')
        print('web')
        print('quit (or exit or stop)')
        print('efile')
        print('unixTime')
        print('killpc')
        print('restartpc')
        print(' ')
        print('For system commands, type help --os')
        print('You may also use help -m name for help with a specific module!')
    elif command == 'help --os':
        print('Here are your system commands:')
        os.system('help')
    elif command == 'help -m help':
        print('help shows the help information for the SoleStormCat terminal.')
        print('You can also use help --os to run the OS help menu.')
    elif command == 'sscpy':
        import SoleStormCatPY.sscPyStandalone as sscpy
        sscpy.fullPythonAppCMD()
    elif command == 'sscpy --gui':
        import SoleStormCatPY.sscPyStandalone as sscpy
        sscpy.fullPythonApp()
    elif command == 'sscpy --upgrade':
        print('Upgrading SoleStormCatPY!')
        print('')
        if pf.system() == 'Windows':
            os.system('py -m pip install --upgrade SoleStormCatPY')
        else:
            os.system('python3 -m pip install --upgrade SoleStormCatPY')
    elif command == 'help -m sscpy':
        print('sscpy is an applacation developed by SoleStormCat Corp. SoleStormCatPY offers many features, and you can visit the GitHub page at https://github.com/solestormcat-corp/solestormcatpy')
        print('You may also run sscpy --gui to run SoleStormCatPY in GUI mode!')
        print('To update SoleStormCatPY, you can run sscpy --upgrade to update.')
    elif command == 'python':
        import SoleStormCatPY.appOpener as appo
        appo.openAppManual('Python')
    elif command == 'help -m python':
        print('python is a coding platform developed by the Python Software Foundation.')
    elif command == 'web':
        import SoleStormCatPY.WebOpen as web
        web.webCMDgui()
    elif command == 'web --tk':
        import SoleStormCatPY.WebOpen as web
        web.webGUI()
    elif command == 'web --db':
        import SoleStormCatPY.WebOpen as web
        print('What website do you want to visit?')
        website = input(' ')
        web.webCMD(website)
    elif command == 'help -m web':
        print('web utilizes the SoleStormCatPY webOpen module to use a web browser.')
        print('You can run web --tk to use a tkinter window for the URL asker.')
        print('You can run web --df to use your defult browser.')
    elif command == 'quit':
        quit()
    elif command == 'exit':
        quit()
    elif command == 'stop':
        quit()
    elif command == 'efile':
        print('Opening an editing app!')
        if pf.system() == 'Windows':
            os.system('Notepad')
        else:
            os.system('nano')
    elif command == 'help -m efile':
            print('efile is a command line that opens a command-line file editor.')
            print('On Windows, Notepad is opened')
            print('On Linux and Mac, nano is opened')
    elif command == 'unixTime':
        import SoleStormCatPY.unixtimecon as unixTime
        unixTime.unixPrint()
        print(' ')
        unixTime.unixConvertor()
    elif command == 'unixTime --time':
        import SoleStormCatPY.unixtimecon as unixTime
        unixTime.unixPrint()
    elif command == 'unixTime --convertor':
        import SoleStormCatPY.unixtimecon as unixTime
        unixTime.unixConvertor()
    elif command == 'help -m unixTime':
        print('unixTime prints the current Unix time, and converts any Unix time into your current time')
        print('You may run unixTime --time to just see the time')
        print('You may run unixTime --convertor to just use the convertor.')
    elif command == 'killpc':
        print('Your computer will be shut off')
        deviceOS = pf.system()
        if deviceOS == 'Windows':
            os.system('shutdown -s -t 0')
        else:
            os.system('sudo shutdown now')
    elif command == 'restartpc':
        print('Your computer will be shut down')
        deviceOS = pf.system()
        if deviceOS == 'Windows':
            os.system('shutdown -r -t 0')
        else:
            os.system('sudo shutdown -r now')
    elif command == 'help -m restartpc':
        print('restartpc reboots the pc.')
    elif command == 'help -m killpc':
        print('killpc shutdowns the computer.')
    else:
        os.system(command)
    print()
    shellOpen()

def shellOpen():
    print(username,'@',hostname)
    command = input(' ')
    shellUse(command)