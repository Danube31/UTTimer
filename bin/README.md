instructions to build binaries for Linux and Windows (pyinstaller python module is required)

1/ Windows (powershell) :

In the folder where all python source files and "resources" folder are located, apply the following command:

      pyinstaller.exe --add-data='resources;resources' --onefile --clean UTTimer.py

2/ Linux (terminal):

In the folder where all python source files and "resources" folder are located, apply the following commands:

      pyinstaller --add-data='resources:resources' --onefile --clean UTTimer.py

Nota : keylogging needs root privileges to be used.

Binaries are available at https://sweetsound9.wixsite.com/uttimer (DL section)

