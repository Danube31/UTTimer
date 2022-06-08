#! /usr/bin/env python
# -*- coding: utf-8 -*-
# GraphicTimerManager: handle dynamic and graphical behaviour of  attached Timers 
# 
# 
#  
import tkinter as tk
from TimerData import TimerData
from Util import *
from DragAndDropLabelsManager import DragAndDropLabelsManager
from AbstractGraphicTimerManager import AbstractGraphicTimerManager
import logging


class GraphicAttachedTimersManager(tk.Toplevel, AbstractGraphicTimerManager):
    # constructor
    def __init__(self, mgr):
        tk.Toplevel.__init__(self)
        AbstractGraphicTimerManager.__init__(self, mgr)
        self.labelNoActiveTimers = None
        
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.setTitle(self.mgr.cfg_file)
        # (re)create Labels        
        nbActiveTimers = self.createLabelTimers()
    # check if detached timers
        if nbActiveTimers >=1:
                 # DragAndDropL Labels Management after update
                dragAndDropTimerTool = DragAndDropLabelsManager(self)
                dragAndDropTimerTool.init()
        else:
            self.labelNoActiveTimers = tk.Label(self, text = 'No active Timers...').grid(padx=50, pady=50)
        # close the window with X
        self.protocol("WM_DELETE_WINDOW", lambda : self.closing_procedure(self.destroy))
        self.bindGTimers()
  
    # bind all       
    def bindGTimers(self):
        self.logger.info('')           
        # handle key binding   
        self.bind('<Key>', lambda event: self.processKeyPressed(event))
    
    # (re)create Labels
    def createLabelTimers(self):
        self.logger.info('')
        # sort by position
        listSortedTimerData = sorted(self.timerConf .TimerDataList, key =lambda TimerData : TimerData.timer_conf[ParamTimerCnf.Position] )
        # create the label for each powerup timer
        index = 0
        for timerData in listSortedTimerData:    
            if timerData.label != None:
                timerData.label.destroy()
                timerData.label = None
            if timerData.isActive() == True:
                fontTimerLabel =  tk.font.Font(family=self.timerConf.general_conf[ParamCnf.TimerFontName], weight=self.timerConf.general_conf[ParamCnf.TimerFontStyle], size = int(self.timerConf.general_conf[ParamCnf.TimerFontSize]))
            
                timerData.label = tk.Label(self, text = timerData.getStrTimerValue() , 
                                                        font = fontTimerLabel,
                                                        foreground = self.timerConf.general_conf[ParamCnf.ColorTimerRGB], 
                                                        bg=timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB] , padx=int(self.timerConf.general_conf[ParamCnf.TimerFontSize]) / 5)
                # vertical or horizontal Disposition
                if int(self.timerConf .general_conf[ParamCnf.Disposition]) == TimerDisposition.VERTICAL.value:
                     timerData.label.grid(row=index, column=0)
                else:      
                     timerData.label.grid(row=0, column=index)     
                # position  in the window
                timerData.gposition = index
                index += 1
        return index         
            
    # evaluate timers position
    def evaluateTimerPosition(self):
        self.logger.info('')
        # sort by position
        listSortedTimerData = sorted(self.timerConf.TimerDataList, key =lambda TimerData : TimerData.timer_conf[ParamTimerCnf.Position] )
        # create the label for each powerup timer
        index = 0
        for timerData in listSortedTimerData: 
            if timerData.isActive() == True:
                if int(self.timerConf.general_conf[ParamCnf.Disposition]) == TimerDisposition.VERTICAL.value:
                     timerData.label.grid(row=index, column=0)
                else:      
                     timerData.label.grid(row=0, column=index)     
            index += 1
            
    #modifiy Disposition
    def changeDisposition(self):
        self.logger.info('')
        if int(self.mgr.UTtimerConfig.general_conf[ParamCnf.Disposition]) != TimerDisposition.DETACHED.value:
            self.evaluateTimerPosition()     
        else:
            self.mgr.buildGTimers()
     
    #modify Font 
    def changeFont(self):  
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList: 
            if timerData.isActive() == True:
                fontTimerLabel =  tk.font.Font(family=self.timerConf.general_conf[ParamCnf.TimerFontName], weight=self.timerConf.general_conf[ParamCnf.TimerFontStyle], size = int(self.timerConf.general_conf[ParamCnf.TimerFontSize]))
                timerData.label.config(font = fontTimerLabel)
     
    #modify color timer text 
    def changeFgColorTimer(self):
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList: 
            if timerData.isActive() == True and self.timerConf.general_conf[ParamCnf.ColorTimerRGB] != '':
                timerData.label.config( foreground = self.timerConf.general_conf[ParamCnf.ColorTimerRGB])
    
    #modify color timer text 
    def changeBgColorTimer(self, name):
        self.logger.info(' name=%s' % name)
        timerData = self.timerConf.getTimerDataFromName(name)
        if timerData.isActive() == True and timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB] != '':
            timerData.label.config(bg=timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB])
            
    # modify timer value
    def changeValue(self, name):
        self.logger.info(' name=%s' % name)
        timerData = self.timerConf.getTimerDataFromName(name)
        if timerData.isActive() == True:
            timerData.label.config(text = timerData.getStrTimerValue())
                                        
    # clean
    def clean(self):
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList:
            if timerData.timer != None and timerData.timer.is_alive():
                timerData.timer.cancel()
        if self.labelNoActiveTimers != None:
            self.labelNoActiveTimers.destroy()
        
    # return size of label
    def getLabelSize(self):
        self.logger.info('')
        for  timerData in self.timerConf.TimerDataList:
            if timerData.label != None:
                return (timerData.label.winfo_width(), timerData.label.winfo_height())   
        return (490, 192) # default
        
    # return timer from gposition
    def getTimerDataFromGPosition(self, gposition):
        self.logger.info('gposition=%s' % gposition)
        for  timerData in self.timerConf.TimerDataList:
            if timerData.isActive() and timerData.gposition == gposition:
                return timerData
  
    #on remove timer
    def removeTimer(self):
        self.logger.info('')
        # replace
        self.evaluateTimerPosition()       

    # setTitle
    def setTitle(self, title):
        self.logger.info('title=%s' % title)
        self.title(title)
        
    # ask before closing application
    def closing_procedure(self, callback, *args, **kwargs):
        self.logger.info('args=%s kwargs=%s' % (args, kwargs))
        self.clean()
        self.mgr.onClosedGtimers()
        callback(*args, **kwargs)
        
    # call by DragAndDrop when drop
    def onDrop(self):
        if tk.messagebox.askyesno("Save configuration", "Timers position have changed. Do you want to save changes ? ", parent=self) == True:
            if self.mgr.optionsEditorMgr == None:
                self.timerConf.saveTimersInformation()
                self.timerConf.saveConfiguration()
            else:
                self.mgr.optionsEditorMgr.saveConfigurationChanges(self.mgr.cfg_file)
