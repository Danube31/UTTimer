1/ releases


V2.4.2:
- resources directory included in bundle
- generation modification

V2.4.1:
- Keylogger configuration fixes and changes
- add audio at start of timer
- improved audio file management (AudioFileWidget)

V2.4.0:
- Keylogger launch on win platform (no admin privilege is required)

V2.3.9.2:
- Keylogger status on the main panel 

V2.3.9.1:
- Recording tool fixes 

V2.3.9:
- Recording tool (need polishing)

V2.3.8:
- Detached timers vs attached timers add/remove polishing
- Font Chooser improvement

V2.3.7 add the following features, 
- Detached timers vs attached timers (need some upgrade to add/remove correctly detached timers)

V2.3.6 add the following features, 
- apply/save enhancement
- null timer name management
- window management 

V2.3.5.2 add the following features, 
- editor fixes (add/remove timer, apply/save)
- front page (facing the tkinter PhotoImage global bug...) 

V2.3.5.1 add the following features, 
- minor fixes
- use winsound SND.ASYNC (windows) and block=False pour playsound

V2.3.5 add the following features, 
- schema xsd

V2.3.4 add the following features, 
- logging  
- apply/save button editor status enhancement

V2.3.3 add the following features, 
- logging  (need more testing)

V2.3.2 add the following features, 
- timer add/remove for more power up  

V2.3.1.1 add the following features, 
- timer add/remove for more power up  (need more testing)

V2.3.1 add the following features, 
- timer inhibition (display and behaviour)

V2.3 add the following features, 
- last elapsed timer indication
- modify timer position (Drag and drop)

V2.1.3, add the following features, 
- configuration XML management updates (recent files)
- keylogger (keylogger.py -h, must have root privilege, i.e sudo like)

V2.1.2, add the following features, 
- configuration XML management (load/save files) , history load

V2.1.1, minor release, 
- fix Entry integer check (validate command + range check + load XML)

V2.1 major release, add the following features
- all parameters may be edited, applied and saved with configuration editor

V2.0.1 alpha, add the following features
- add more parameters to General Information Tab (general parameters)
- add necessary Timer Tab parameters to test General Information Tab
- apply/save better management (To Be Continued)
- saved configuration xml dump (to check) 
- add FontChooser module
- add Util module
- better class structure (add virtuam abstract class to manage General Information Tab and Timer Tab

V2.2, add the following features, 
- configuration XML management updates (fix)
- take into account web latency to improve initial timer value accuracy
- croos platform (linux/windows) :  win platform for colormap playsound (Linux)/winsound (Windows, wav audio only)

V2.1: add the following features
- configuration parameters edition with GUI (modify, save)

V2: add the following features
- speech to text commands (with python SpeechRecognition module)
- structural enhancement (main by adding a general manager)

V1.1: add the following features
- timers management (local keystrokes, Timers)
- sound event integration (playsound and threads)
- graphical enhancements

V1: fisrt release
- XML based configuration file
- GUI based on tkinter

2/ Installation (if intended development):
- mandatory modules:
    - playsound (linux)
        - pip install playsound
    - winsound (Windows platform)
    - colorama (colorerd print)
        - pip install colorama
    - pyaudio (microphone management)
        - Windows:
            - download https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio whl package according to your python version)
            - pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl (for python 3.10)
        - linux (ubuntu):
            - sudo apt update
            - sudo apt install python3-pyaudio
        - linux (fedora):
            - sudo dnf install python3-pyaudio
    - SpeechRecognition (speech to text)
        - pip install SpeechRecognition
    - lxml (windows)
        - pip install lxml
    


3/ exploitation: 

check bin directory for instruction. Check also available handbook.
