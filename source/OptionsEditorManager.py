#! /usr/bin/env python
# -*- coding: utf-8 -*-
# OptionsEditorManager: handle edition of configuration parameters 
# 
# 
#  
import tkinter as tk
from tkinter.ttk import Notebook
from TimerData import TimerData
from Util import *
from GeneralInformationTab import GeneralInformationTab
from TimerTab import TimerTab
from InfoTab import DataVarTab
import os
import logging
        

class OptionsEditorManager(tk.Toplevel):
    # constructor
    def __init__(self, mgr):
        super().__init__()
        self.mgr = mgr;
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.resetAllTimers()
        self.timerConf = mgr.UTtimerConfig
        self.listActiveTimers =  self.timerConf.getActiveTimersList()
        
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        
        self.setTitle(self.mgr.cfg_file)
        # notebook
        self.notebook = Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill = 'both')
        # bind callback if tab is changed
        self.notebook.bind('<<NotebookTabChanged>>', self.notebookTabchanged)
        # one frame per tab
        self.frames = []
        self.generalInformationTab  = None
        # list of timer tabs
        self.timerTabs = []
        self.statusParams = ParamStatus.NONMODIFIED
        self.isModified = False
        
        # create frames
        
        # general information notebook tab
        self.frames.append(tk.Frame(self.notebook, width=600, height=280))
        self.frames[0].pack(fill='both', expand=True)
        self.notebook.add(self.frames[0], text='General Information')
        
        # create the tabs for general parameters and each powerup parameter
        for index, timerData in enumerate(self.timerConf.TimerDataList):
            self.frames.append(tk.Frame(self.notebook, width=400, height=280))
            self.frames[index+1].pack(fill='both', expand=True)
            # add Tab to notebook
            self.notebook.add(self.frames[index+1], text=timerData.timer_conf[ParamTimerCnf.Name])
            self.logger.debug("add notebook tab name %s index %d" % (timerData.timer_conf[ParamTimerCnf.Name], index + 1))
            # build tab contents
            self.buildTimerTab(self, timerData, index+1)
                    
        # build general information tab contents
        self.buildGeneralInformationTab(self)
        
        # buttons Close, Apply, Save
        self.buttonClose = tk.Button(self, text="Close", command=lambda : self.closing_procedure(self.destroy))
        self.buttonClose.pack(padx=10, pady=10, side= 'left' )
        self.buttonApply = tk.Button(self, text="Apply", command=self.applyConfigurationChanges, state=tk.DISABLED)
        self.buttonApply.pack(padx=10, pady=10, side= 'left' )
        self.buttonSave = tk.Button(self, text="Save", command=lambda : self.saveConfigurationChanges(self.mgr.cfg_file), state=tk.DISABLED)
        self.buttonSave.pack(padx=10, pady=10, side= 'left' )
        self.buttonSaveAs = tk.Button(self, text="Save as", command=lambda : self.pickFileAndSave('Save configuration file', self.mgr.cfg_file), state=tk.DISABLED)
        self.buttonSaveAs.pack(padx=10, pady=10, side= 'left' )
        # button Add timer
        self.buttonAddTimer = tk.Button(self, text="Add timer", command= self.addTimer)
        self.buttonAddTimer.pack(padx=50, pady=10, side= 'left' )
        
        # close the window with X
        self.protocol("WM_DELETE_WINDOW", lambda : self.closing_procedure(self.destroy))
        
    # bind all       
    def bind(self):
        self.logger.info('')
        self.generalInformationTab.bind()
        for timerTab in self.timerTabs:
            timerTab.bind()
        
    # build General Information Tab
    def buildGeneralInformationTab(self, omgr):
        self.logger.info('')
        self.generalInformationTab =  GeneralInformationTab(omgr, self.frames[0])
        self.generalInformationTab.init()
        
    # build Timer Tab
    def buildTimerTab(self, omgr, timerData, index):
        self.logger.info('name=%s index=%d ' %(timerData.timer_conf[ParamTimerCnf.Name], index))
        timerTab = TimerTab(omgr, self.frames[index], timerData.timer_conf[ParamTimerCnf.Name])
        timerTab.init()
        self.timerTabs.append(timerTab)
        return timerTab
        
        
    # ask before closing application
    def closing_procedure(self, callback, *args, **kwargs):
        self.logger.info('args=%s kwargs=%s' % (args, kwargs))
        if self.isConfigurationModificationApplied() == True:  
            if tk.messagebox.askyesno("Quit", "Some parameters have been modified and applied: do you really want to close ? ", parent = self):
                self.clean()
                self.mgr.onClosedEditor()
                callback(*args, **kwargs)
        else:
            self.clean()
            self.mgr.onClosedEditor()
            callback(*args, **kwargs)
            
     #pick/new conf file and save
    def pickFileAndSave(self, title, initialfile):
        self.logger.info('title=%s initlalfile=%s' % (title,initialfile))
        filename = tk.filedialog.asksaveasfilename(title=title, initialfile=os.path.basename(initialfile), initialdir = os.path.dirname(initialfile), filetypes=SelectFile.XMLFILES)
        self.logger.info(filename)
        if filename != ():
        
                root, ext = os.path.splitext(filename)
                if not  '.xml' in ext:
                    filename += '.xml'
                self.logger.info('save to %s'% filename)
                self.saveConfigurationChanges(filename)
            
        
    # apply options modification (not saved to XML file)
    def applyConfigurationChanges(self):
        self.logger.info('')
        if self.checkTimersName() == False:
                # apply
                self.generalInformationTab.applyConfigurationChanges()
                for timerTab in self.timerTabs:
                    timerTab.applyConfigurationChanges()
                self.statusParams = ParamStatus.APPLIED
                self.buttonApply.config(state=tk.DISABLED)
                listActiveTimers = self.timerConf.getActiveTimersList()
                if listActiveTimers != self.listActiveTimers:
                        self.mgr.buildGTimers()
                        self.listActiveTimers = listActiveTimers
                self.isModified = False
                result = True
        else:
                tk.messagebox.showwarning('Warning', 'Timers need name !', parent = self)
                result = False
        return result
        
    
    # save options window (applied and save  to XML file)
    def saveConfigurationChanges(self, filename):
        self.logger.info('filename=%s' % filename)
        # save if apply OK
        if self.applyConfigurationChanges() == True:
                self.setTitle(filename)
                # save to XML file
                self.timerConf.saveConfiguration(filename) 
                # saved conf
                self.statusParams = ParamStatus.SAVED
                # disable button 
                self.buttonApply.config(state=tk.DISABLED)
                # disable button
                self.buttonSave.config(state=tk.DISABLED)
                # disable button
                self.buttonSaveAs.config(state=tk.DISABLED)
        
    # called when at least one parameter has been modified
    def configurationModified(self,  name = None, index = None, mode = None):
        self.logger.debug('')
        isModified = self.isModified | self.generalInformationTab.isGeneralInfoConfModified()
        for timerTab in self.timerTabs:
            isModified |= timerTab.isTimerConfModified()
        if isModified == True:
                self.statusParams = ParamStatus.MODIFIED
                self.buttonApply.config(state=tk.NORMAL)
                self.buttonSave.config(state=tk.NORMAL)
                self.buttonSaveAs.config(state=tk.NORMAL)
        else:
                self.statusParams = ParamStatus.NONMODIFIED
                self.buttonApply.config(state=tk.DISABLED)
                self.buttonSave.config(state=tk.DISABLED)
                self.buttonSaveAs.config(state=tk.DISABLED)
            
    # called when at least one parameter has been modified
    def isConfigurationModificationApplied(self):
        self.logger.info('')
        return self.statusParams == ParamStatus.APPLIED
 
    # clean data
    def clean(self):
        self.logger.info('')
        self.editing = False
        self.generalInformationTab.clean()
        for timerTab in self.timerTabs:
            timerTab.clean()
                                
    # setTitle
    def setTitle(self, filename):
        self.logger.info('filename=%s' % filename)
        self.title('configuration edition: %s' % filename)
       
        
    #modifiy Disposition
    def changeDisposition(self):
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeDisposition()
     
    #modify Font 
    def changeFont(self):  
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeFont()
     
    #modify color timer text 
    def changeFgColorTimer(self):
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeFgColorTimer()
            
    # modify color bg font
    def changeBgColorTimer(self, name):
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeBgColorTimer(name)
                
    # timer presence
    def changeActiveTimer(self, name):
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeActiveTimer(name)
                
    #modify value
    def changeValue(self, name):
        self.logger.info('')
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.changeValue(name)
  
    #modify status
    def changeExternalKeyLogger(self):
        self.logger.info('')
        self.mgr.manageKeyLogger(not(self.timerConf.general_conf[ParamCnf.ExternalKeyLogger]))
    
    #get tab name from tabs' name
    def getNameFromTimeTabs(self, name):
        self.logger.info('name=%s' % name)
        for timerTab in self.timerTabs:
                if timerTab.name == name:
                        return timerTab
                
    #modify name
    def changeName(self, previousName):
        self.logger.info('previousName=%s' % previousName)
        timerTab = self.getNameFromTimeTabs(previousName)
        timerTab.name = timerTab.Var[ParamTimerCnf.Name].var.get()
        for timerData in self.timerConf.TimerDataList:
                if timerData.timer_conf[ParamTimerCnf.Name] == timerTab.name:
                        break
        self.logger.info('tab new name : %s index %d' % (timerTab.name, timerData.index))
        self.notebook.tab(timerData.index+1, text= timerTab.name)
        
    #add  timer
    def  addTimer(self):
        self.logger.info('')
        timerData = self.timerConf.createNewTimer()
        index = self.timerConf.getTimerDataListSize()
        self.frames.append(tk.Frame(self.notebook, width=400, height=280))
        self.frames[index].pack(fill='both', expand=True)
        # add Tab to notebook
        self.notebook.add(self.frames[index], text=timerData.timer_conf[ParamTimerCnf.Name])
        # build tab contents
        timerTab = self.buildTimerTab(self, timerData, index)
        self.logger.debug("add notebook tab name %s index %d" % (timerData.timer_conf[ParamTimerCnf.Name], index))
        # bind events
        timerTab.bind()
        self.notebook.select(index)
        if self.timerConf.getTimerDataListSize() == 1:
                self.generalInformationTab.update()
        # configuration has been modified
        self.isModified = True
        self.configurationModified()
        self.applyConfigurationChanges()

    # remove timer
    def removeTimer(self, name):
        self.logger.info('name=%s' % name)
        for timerData in self.timerConf.TimerDataList:
                self.logger.debug("name %s index %d" % (timerData.timer_conf[ParamTimerCnf.Name], timerData.index))
        timerData = self.timerConf.getTimerDataFromName(name)  
        self.logger.debug("remove notebook tab %d" % timerData.index)
        index = timerData.index
        self.frames.pop(index)
        for item in self.notebook.winfo_children():
                if str(item) == self.notebook.select():
                        self.logger.debug("destroy tab %s index %d" % (str(item), index))
                        item.destroy()
        position = int(timerData.timer_conf[ParamTimerCnf.Position])
        self.timerConf.removeTimer(timerData)
        # after removing TimerData from conf list, shift position of following timer
        for oTimerData in self.timerConf.TimerDataList:
                oPosition = int(oTimerData.timer_conf[ParamTimerCnf.Position])
                if oPosition > position:
                        oTimerData.timer_conf[ParamTimerCnf.Position] = str(oPosition - 1)
        self.logger.debug(self.timerConf.TimerDataList)
        timerTab = self.getNameFromTimeTabs(name)
        self.timerTabs.remove(timerTab)
        # reevaluate tab index
        for timerData in self.timerConf.TimerDataList:
                if timerData.index > index:
                        timerData.index -= 1
        self.isModified = True
        self.configurationModified()
        if self.mgr.gTimersManager:
                self.mgr.gTimersManager.removeTimer()
        self.applyConfigurationChanges()
        
    # called when tab changed
    def notebookTabchanged(self, event):
        self.logger.info('')
        indexSelectedTab = self.notebook.index(self.notebook.select())
        self.logger.debug('tab %d selected' % indexSelectedTab)
        if indexSelectedTab == 0: # generalInformationTab
                self.generalInformationTab.textFontDemo.unfreeZe()
        else:
                self.generalInformationTab.textFontDemo.freeZe()

    # check it at least a timer name is empty
    def checkTimersName(self):
        result = False
        for timerTab in self.timerTabs:
                if timerTab.timerNameVarLenght() == 0:
                        result = True
                        break;
        return result
