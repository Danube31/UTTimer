instructions to build binaries for Linux and Windows (pyinstaller python module is required)

1/ Windows (powershell) :

In the folder where all python file and "resources" folder are located, apply the followind command

pyinstaller.exe --onefile --clean keylogger.py

Copy generated binary file KeyLogger located in "dist" sub folder to "resources" folder

then, apply the following command

pyinstaller.exe --add-data='resources;resources' --onefile --clean UTTimer.py

2/ Linux (terminal):

In the folder where all python file and "resources" folder are located, apply the followind command

pyinstaller --onefile --clean keylogger.py

pyinstaller --add-data='resources;resources' --onefile --clean UTTimer.py


Binaries are available at https://sweetsound9.wixsite.com/uttimer (DL section)

