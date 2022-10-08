instructions to build binaries for Linux and Windows (pyinstaller python module is required)

1/ Windows (powershell) :

In the folder where all python file and "resources" folder are located, apply the following command:

      pyinstaller.exe --onefile --clean keylogger.py

Copy generated binary file keyLogger.exe located in "dist" sub folder to "resources" folder

then, apply the following command

      pyinstaller.exe --add-data='resources;resources' --onefile --clean UTTimer.py
      Cancel changes

2/ Linux (terminal):

In the folder where all python file and "resources" folder are located, apply the following commands:

      pyinstaller --onefile --clean keylogger.py

      pyinstaller --add-data='resources:resources' --onefile --clean UTTimer.py

      chmod +x keylogger UTTimer

keylogger needs roots privilege to run.

Binaries are available at https://sweetsound9.wixsite.com/uttimer (DL section)

