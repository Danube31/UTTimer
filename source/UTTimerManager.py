#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  UTTimerManager.py : main manager
#  

import tkinter as tk
import os
import subprocess
import sys
from TimerConfiguration import TimerConfiguration
from GraphicDetachedTimersManager import GraphicDetachedTimersManager
from GraphicAttachedTimersManager import GraphicAttachedTimersManager
from SpeechToTextUTTimer import SpeechToCommand
from OptionsEditorManager import OptionsEditorManager
from Util import *
from functools import partial
from threading import Timer, Thread
import socket
import time
from datetime import datetime
import logging
import lxml                                                                    
from lxml import etree


# UTTimers management
class UTTimerManager:
    
    HISTORY_FILENAME = 'resources/config_history'
    SCHEMA_XSD_FILENAME = 'resources/timerConfig.xsd'  
    VERSION='V2.4.1'
    KEYLOGGER= "keylogger"
    
    # constructor
    def __init__(self, platform):
        self.ws = None
        self.gTimersManager = None
        self.speechToCmd = None
        self.cfg_file = None
        self.last_cfg_file = self.cfg_file
        self.optionsEditorMgr = None
        self.socketThread = None
        self.clientSocket = None
        self.xsd_file = UTTimerManager.SCHEMA_XSD_FILENAME
        self.labelKeyLogger = None
        self.labelKeyLoggerStatus = None
        self.platform = platform
        self.tcpsock = None
        
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.UTtimerConfig = TimerConfiguration(self)
        self.UTtimerConfig.init()
        self.checkHistoryFile()
        # main window
        self.ws = tk.Tk()
        self.setGUITitle()        
        # close window with X: clean application
        self.ws.protocol('WM_DELETE_WINDOW',  lambda : self.closing_procedure(self.ws.destroy))
        # bind keystroke to activate/stop timers
        self.bindGTimers()
        # create image for keylogging status
        self.imgOffRed = tk.PhotoImage(file='resources/DomeLight_offRed-30px.png')
        self.imgOnRed = tk.PhotoImage(file='resources/DomeLight_onRed-30px.png')
        self.imgOnGreen = tk.PhotoImage(file='resources/DomeLight_onGreen-30px.png')
        
    
    # check history file
    def checkHistoryFile(self):
        self.logger.info('')
        tabfiles = []
        modified = False 
        try:
            with open(UTTimerManager.HISTORY_FILENAME, 'r') as historyFile:
                tabfiles = historyFile.readlines()
                #check history file content
                for xmlfile in tabfiles.copy():
                    root, ext = os.path.splitext(xmlfile.strip())
                    if not  '.xml' in ext:
                        self.logger.warning('Configuration file %s is not valid, contains non XML file %s, skip' % (UTTimerManager.HISTORY_FILENAME, xmlfile.strip()))
                        tabfiles.remove(xmlfile)
                        modified = True
                    elif not os.path.exists(xmlfile.strip()):
                        tabfiles.remove(xmlfile)
                        modified = True
                        self.logger.warning('Configuration file %s doesn\'t exist anymore' % xmlfile.strip())
        except FileNotFoundError:
            self.logger.error('History file %s doesn\'t exist' % UTTimerManager.HISTORY_FILENAME)
        if modified == True:
            try:
                with open(UTTimerManager.HISTORY_FILENAME, 'w') as historyFile:
                    historyFile.write(''.join(tabfiles))
            except FileNotFoundError:
                self.logger.error('History file %s doesn\'t exist' % UTTimerManager.HISTORY_FILENAME)
                
    # check XML file
    def checkFile(self, cfg_file, xsd_file = None):
        self.logger.info('cfg_file=%s, xsd_file=%s' % (cfg_file, xsd_file))
        if not os.path.exists(cfg_file):
            self.logger.error('Configuration file %s doesn\'t exist' % cfg_file)
            sys.exit(-1)
        else:
            root, ext = os.path.splitext(cfg_file)
            if not  '.xml' in ext:
                self.logger.error('Configuration file %s is not an valid XML file' % cfg_file)
                sys.exit(-1)
            else:
                self.checkXSD(cfg_file, xsd_file)
           
    # check schema XML file  
    def checkXSD(self, cfg_file, xsd_file = None):
        self.logger.info('')
        doc_xsd = None
        if xsd_file != None:
            self.xsd_file = xsd_file
        self.logger.info('xsd_file=%s' % self.xsd_file)
        try:
            with open(self.xsd_file) as schemaXsdFile:                                                
                doc_xsd = etree.parse(schemaXsdFile)   
        except FileNotFoundError:
            self.logger.error('Xsd file file %s doesn\'t exist' % self.xsd_file)
        except PermissionError:
            self.logger.error('Xsd file %s can not be opened' % self.xsd_file)
        self.logger.info("Validating schema : %s" % self.xsd_file)
        try:                                                                        
            schema = etree.XMLSchema(doc_xsd)                                           
        except lxml.etree.XMLSchemaParseError as e:       
            self.logger.error('Error parsing  %s %s' % (e, self.xsd_file))                                                        
            sys.exit(-1)
        self.logger.info("Schema : %s OK" % self.xsd_file)
        try:
            with open(cfg_file) as confFile:                                                
                doc_cnfFile= etree.parse(confFile) 
        except FileNotFoundError:
            self.logger.error('Configuration file file %s does not exist' % cfg_file)                                                     
            sys.exit(-1)
        except PermissionError:
            self.logger.error('Configuration file %s cannot be opened' % cfg_file)                                                       
            sys.exit(-1)
            
        self.logger.info("Validating document %s"  % cfg_file)                                            
        try:                                                                        
            schema.assertValid(doc_cnfFile)                                                 
        except lxml.etree.DocumentInvalid as e:      
            self.logger.error('Error validating  %s %s' % (e, cfg_file))   
            sys.exit(-1)  
    
    # load checked file
    def loadFile(self, cfg_file):
        self.logger.info('cfg_file=%s' % cfg_file)
        self.cfg_file = cfg_file
        self.UTtimerConfig.load()
        self.UTtimerConfig.print()

    # append last saved file
    def manageConfigurationFileHistory(self):
        self.logger.info('')
        try:
            with open(UTTimerManager.HISTORY_FILENAME, 'a') as historyFile:
                if self.cfg_file != self.last_cfg_file:
                    historyFile.write(self.cfg_file+'\n')
                    self.last_cfg_file  = self.cfg_file
        except FileNotFoundError:
            self.logger.error('Configuration file %s doesn\'t exist' % self.cfg_file)
        except PermissionError:
            self.logger.error('Configuration file %s can not be appended' % self.cfg_file)
        else:
            # reload file to clean duplicate
            try:
                tabfiles = []
                with open(UTTimerManager.HISTORY_FILENAME, 'r') as historyFile:
                    tabfiles = historyFile.readlines()
            except FileNotFoundError:
                self.logger.error('Configuration file %s doesn\'t exist' % self.cfg_file)
            else: 
                # remove duplicate
                for xmlfile in tabfiles[:-1].copy():
                    if xmlfile == tabfiles[-1]:
                        tabfiles.remove(xmlfile)
                try:
                    with open(UTTimerManager.HISTORY_FILENAME, 'w') as historyFile: 
                        historyFile.write(''.join(tabfiles))
                except FileNotFoundError:
                    self.logger.error('Configuration file %s doesn\'t exist' % self.cfg_file)
                except PermissionError:
                    self.logger.error('Configuration file %s can not be written' % self.cfg_file)
                
    # appplication info
    def about(self):
        tk.messagebox.showinfo('UT Timer', 'UT Timer aims at providing timers to help managing power up in UT\n%s\ncopyright [TTF]psy - 2022' % UTTimerManager.VERSION, parent=self.ws)
    
    # ask before closing application
    def closing_procedure(self, callback, *args, **kwargs):
        self.logger.info('args=%s kwargs=%s' % (args, kwargs))
        if self.optionsEditorMgr != None and self.optionsEditorMgr.isConfigurationModificationApplied() == True:  
            if tk.messagebox.askyesno("Quit", "Some parameters have been modified and applied: do you really want to close ? ", parent=self.ws):
                callback(*args, **kwargs)
                self.clean()
        elif tk.messagebox.askyesno("Quit", "Do you really want to close ? ", parent=self.ws):
            callback(*args, **kwargs)
            self.clean()
            sys.exit()
    
    # clean application before exiting
    def clean(self):
        self.logger.info('')
        # eventually clean GraphicTimersManager   
        if self.gTimersManager != None:
            self.gTimersManager.clean()
        # eventually clean OptionsEditorManager
        if self.optionsEditorMgr != None:
            self.optionsEditorMgr.clean()
        # clean SpeechToCommand   
        self.speechToCmd.clean()
        # key logger connection is closed    
        self.stopKeyLoggerConnection()
    
    # options edition
    def optionsEdition(self):
        self.logger.info('')
        if self.optionsEditorMgr == None:
            self.optionsEditorMgr = OptionsEditorManager(self)
            self.optionsEditorMgr.init()
            self.optionsEditorMgr.bind()
            self.editM.entryconfig(1, state=tk.DISABLED)
            
    # on Editor close
    def onClosedEditor(self):
        self.logger.info('')
        self.optionsEditorMgr = None
        self.editM.entryconfig(1, state=tk.NORMAL)
        
    # on GTimers close
    def onClosedGtimers(self):
        self.logger.info('')
        self.gTimersManager = None
        
    # build HMI
    def buildGUI(self, loadTimers):
        self.logger.info('loadTimers=%d', loadTimers)
        # menubar creation (FILE, EDIT, ABOUT)
        menubar = tk.Menu(self. ws, background='grey', foreground='black', activebackground='white', activeforeground='black')  
        self.fileM = tk.Menu(menubar, tearoff=False)  
        # close application with Exit item
        # File->...
        menubar.add_cascade(label="File", menu=self.fileM)  
        # File->Load configuration...->Browse...
        self.loadCnf = tk.Menu(self.fileM, tearoff=False)
        self.loadCnf.add_command(label='Browse...', command = self.loadFileFromFileChooser)
        self.loadCnf.add_separator()
        # File->Load configuration...->[list of recent files]
        try:
            with open(UTTimerManager.HISTORY_FILENAME, 'r') as file:
                tabfiles = file.readlines()
                rt =  tabfiles.copy()
                rt.reverse()
                #check history file content
                for xmlfile in rt:
                    self.loadCnf.add_command(label=xmlfile.strip(), command = partial(self.loadFileFromMenu, xmlfile.strip()))
        except FileNotFoundError:
            self.logger.error('Configuration file %s doesn\'t exist' % UTTimerManager.HISTORY_FILENAME)
        # File->Load configuration...
        self.fileM.add_cascade(label="Load configuration...", menu=self.loadCnf)  
        # File->New configuration
        self.fileM.add_command(label="New configuration", command= self.newConfiguration)  
        # File->Exit
        self.fileM.add_command(label="Exit", command= lambda : self.closing_procedure(self.ws.destroy))  
        # Edit->...
        self.editM = tk.Menu(menubar, tearoff=False)  
        # Edit->Options
        self.editM.add_command(label="Configuration", command = self.optionsEdition) 
        if self.cfg_file == None:
            self.editM.entryconfig(0, state=tk.DISABLED)
        menubar.add_cascade(label="Edit", menu=self.editM)
        # About->...
        helpM = tk.Menu(menubar, tearoff=False)  
        helpM.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpM)  
        #update menu
        self.ws.config(menu=menubar)
        if loadTimers == True:
            # timers management (dynamic and graphical)
            self.buildGTimers()
        
        global img  # bug PhotoImage...
        img = tk.PhotoImage(file='resources/UTlogo50.png')
        tk.Label(self.ws, image=img).pack()
        
        self.labelKeyLogger = tk.Label(self.ws, text='Keylogger')
        self.labelKeyLogger.pack()
        self.labelKeyLoggerStatus = tk.Label(self.ws, image=self.imgOffRed)
        self.labelKeyLoggerStatus.pack()
        
        if loadTimers == True:
            self.manageKeyLogger(not(self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger]))
        
    # timers management (dynamic and graphical)
    def buildGTimers(self):
        self.logger.info('')
        if self.gTimersManager != None:
            self.gTimersManager.clean()
            self.logger.debug('')
            self.gTimersManager.destroy()
        if int(self.UTtimerConfig.general_conf[ParamCnf.Disposition]) != TimerDisposition.DETACHED.value:
            self.gTimersManager = GraphicAttachedTimersManager(self)
        else:
            self.gTimersManager = GraphicDetachedTimersManager(self)
        self.gTimersManager.init()
        
        self.activateSpeechToCommand()
        self.editM.entryconfig(0, state=tk.NORMAL)
        
    # load a configuration file from menu and apply it
    def loadFileFromMenu(self, filename):
        # memorize previous status of externalKeyLogger setup
        if self.cfg_file == None:
            externalKeyLogger = False
        else:
            externalKeyLogger = self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger]
        self.logger.info('filename=%s', filename)
        self.cfg_file = filename
        # check schema
        self.checkXSD(self.cfg_file)
        # clear the Timerconfiguration class
        self.UTtimerConfig.clear()
        # load XML file in memory
        self.UTtimerConfig.load()
        # print  XML file in memory
        self.UTtimerConfig.print()
        # rebuilg GUI with new configuration
        self.buildGTimers()
        # conf history update
        self.manageConfigurationFileHistory()
        # update recent configuration file
        self.updateItemsMenuLoadConf()
        # update keylogger setup if changed in the new configuration
        self.manageKeyLogger(externalKeyLogger)
        # update key list
        self.sendKeysList()
        
    # update menu on file loading
    def updateItemsMenuLoadConf(self):
        self.logger.info('')
        try:
            with open(UTTimerManager.HISTORY_FILENAME, 'r') as file:
                tabfiles = file.readlines()
                rt =  tabfiles.copy()
                rt.reverse()
                for item in  rt:
                    self.logger.debug(item.strip())
                # destroy item after separator
                self.loadCnf.delete(2, len(tabfiles)+1)
                #check history file content (except for the first)
                # use partial rather than lambda here (menu bug)
                for xmlfile in rt[1:]:
                    self.loadCnf.add_command(label=xmlfile.strip(), command = partial(self.loadFileFromMenu, xmlfile.strip()))
        except FileNotFoundError:
            self.logger.error('Configuration file %s doesn\'t exist' % UTTimerManager.HISTORY_FILENAME)
        
    # load file from file chooser tk widget
    def loadFileFromFileChooser(self):
        self.logger.info('')
        filename = tk.filedialog.askopenfilename(initialdir = '.', title='Open configuration file', filetypes=SelectFile.XMLFILES)
        if filename != () and os.path.exists(filename):
            self.logger.info('loaded file %s' % filename)
            self.loadFileFromMenu(filename)
                    
    # prepare speech recognition to text command 
    def prepareSpeechToCommand(self):
        self.logger.info('')
        self.speechToCmd = SpeechToCommand()
        self.speechToCmd.init()
            
    # if set up, activate speech recognition to text command 
    def activateSpeechToCommand(self): 
        self.logger.info('')
        if self.UTtimerConfig.general_conf[ParamCnf.ActiveSpeechToCommand] == True:
            self.speechToCmd.activateSpeechToCommand(self.gTimersManager)
    
    # set  GUI Title
    def setGUITitle(self, cfg_file = None):
        self.logger.info('')
        if cfg_file == None:
            self.ws.title('UT Timer ')
        else:
            self.ws.title('UT Timer : % s' % cfg_file)
            
    # mainloop
    def mainloop(self):
        self.logger.info('')
        self.ws.mainloop()
    
    # process messages sent by client
    def processMessage(self, message):
        self.logger.info('message=%s' % message)
        if self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger] == True:
            self.gTimersManager.processKeyChar(message[0])

    # thread procedure to handle client connections/messages
    def clientConnexionThread(self):
        self.logger.info('')
        port = int(self.UTtimerConfig.general_conf[ParamCnf.KeyLoggerPort])
        if self.tcpsock == None:
            self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.tcpsock.bind(("", port))
            self.tcpsock.listen(10)
        while self.loopKeyLogger == True:
            self.logger.info( "listening on port %d ..." % port)
            (self.clientSocket, (self.ipclient, port_client)) = self.tcpsock.accept()
            self.updateKeyLoggerStatus()
            self.logger.info( 'client %s connected' % self.ipclient)
            # send keys list
            self.sendKeysList()
            # # send list of authorized keys for external key logger
            self.clientSocket.send(self.UTtimerConfig.getKeysList().encode())
            while  self.loopKeyLogger == True:
                try:
                        # test if client still connected
                        message = self.clientSocket.recv(4096).decode()
                        if not message:
                                self.logger.warning("clientConnexionThread : client %s deconnexion " % self.ipclient)
                                self.clientSocket = None
                                self.updateKeyLoggerStatus()
                                break
                        else:
                                self.processMessage(message)
                except socket.error:
                        # fin du thread
                        self.logger.warning("clientConnexionThread : client %s deconnexion on socket error" % self.ipclient)
                        self.clientSocket = None
                        self.updateKeyLoggerStatus()
                        break
        if self.clientSocket != None:
            self.clientSocket.close()
        self.logger.info( "Shutdown thread server")
            
    # send keys list
    def sendKeysList(self):
        self.logger.info('')
        if self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger] == True and self.clientSocket != None: 
            self.logger.debug('send keys updates to client %s' % self.ipclient)
            self.clientSocket.send(self.UTtimerConfig.getKeysList().encode())
         
    # update KeyLoggerStatus if necessary
    def updateKeyLoggerStatus(self):
        self.logger.info('')
        if self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger] == True:
            if self.clientSocket == None:
                self.logger.debug('')
                self.labelKeyLoggerStatus.config(image=self.imgOnRed)
            else:
                self.logger.debug('')
                self.labelKeyLoggerStatus.config(image=self.imgOnGreen)
        elif self.labelKeyLoggerStatus != None:
                self.logger.debug('')
                self.labelKeyLoggerStatus.config(image=self.imgOffRed)
                  
    # kill keylogger process (win only => taskkill
    def killKeyLoggerProcess(self):
        self.logger.info('')
        cmd = 'taskkill /f /im ' + UTTimerManager.KEYLOGGER + '.exe'
        self.logger.debug('launch ' + cmd)
        subprocess.call(cmd)
        
    # launch socket  for key logger
    def activateKeyLoggerInterface(self):
        self.logger.info('')
        if self.socketThread == None:
           # launch server thread
            self.loopKeyLogger = True
            self.socketThread = Thread(target=self.clientConnexionThread)
            self.socketThread.daemon = True
            self.socketThread.start()
            
            # launch key logger
            if 'win' in self.platform:
                self.killKeyLoggerProcess()
                cmd = UTTimerManager.KEYLOGGER + '.exe -s localhost -p %s' % self.UTtimerConfig.general_conf[ParamCnf.KeyLoggerPort] 
                self.logger.debug('launch ' + cmd)
                subprocess.Popen(cmd, shell=True)
                
    #manage keylogger activation/shutdown
    def manageKeyLogger(self, externalKeyLogger):
        if self.UTtimerConfig.general_conf[ParamCnf.ExternalKeyLogger] == True:
            if externalKeyLogger == False:
                self.activateKeyLoggerInterface()
                self.updateKeyLoggerStatus()
        else:
            if externalKeyLogger == True:
                self.stopKeyLoggerConnection()
                self.updateKeyLoggerStatus()
                
    # stop key logger connection
    def stopKeyLoggerConnection(self):
        self.logger.info('')
        self.loopKeyLogger = False
        self.socketThread = None
        if 'win' in self.platform:
            self.killKeyLoggerProcess()
        
    # configuration creation
    def newConfiguration(self):
        self.logger.info('')
        if self.gTimersManager != None:
            self.gTimersManager.clean()
            self.logger.debug('')
            self.gTimersManager.destroy()
            self.gTimersManager = None
        if self.optionsEditorMgr != None:
            self.optionsEditorMgr.destroy()
            self.optionsEditorMgr = None
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.cfg_file = 'newConfigFile_%s.xml' % now
        self.UTtimerConfig.newConfiguration()
        self.optionsEdition()
        
    # bind all  keystroke
    def bindGTimers(self):
        self.logger.info('')      
        # handle key binding  
        self.ws.bind('<Key>', lambda event: self.processKeyPressed(event))
    
    # dispacth to Graphic Timers manager
    def processKeyPressed (self, event):
        self.logger.info('event.char=%s' % event.char)
        if self.gTimersManager != None:
            self.gTimersManager.processKeyChar(event.char)
