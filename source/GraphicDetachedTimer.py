#! /usr/bin/env python
# -*- coding: utf-8 -*-
# GraphicDetachedTimerManager: handle dynamic and graphical behaviour of a detached timer
# 
# 
#  
import tkinter as tk
from TimerData import TimerData
from Util import *
import logging


class GraphicDetachedTimer(tk.Toplevel):
    # constructor
    def __init__(self, mgr, name):
        super().__init__()
        self.mgr = mgr
        self.timerConf = mgr.UTtimerConfig
        self.timerData = self.timerConf.getTimerDataFromName(name)
        
    # initialization
    def init(self, ):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.setTitle( self.timerData.timer_conf[ParamTimerCnf.Name])
        self.createLabelTimer()
        self.bindGTimers()
        # close the window with X
        self.protocol("WM_DELETE_WINDOW", lambda : self.closing_procedure(self.destroy))
  
    # bind all       
    def bindGTimers(self):
        self.logger.info('')           
        # handle key binding   
        self.bind('<Key>', lambda event: self.mgr.gTimersManager.processKeyPressed(event))
    
    # (re)create Labels
    def createLabelTimer(self):
        self.logger.info('')
        if self.timerData.label != None:
            self.timerData.label.destroy()
            self.timerData.label = None
        fontTimerLabel =  tk.font.Font(family=self.timerConf.general_conf[ParamCnf.TimerFontName], weight=self.timerConf.general_conf[ParamCnf.TimerFontStyle], size = int(self.timerConf.general_conf[ParamCnf.TimerFontSize]))
        self.logger.debug('Label %s creation text=%s' %(self.timerData.timer_conf[ParamTimerCnf.Name], self.timerData.getStrTimerValue()))
        self.timerData.label = tk.Label(self, text = self.timerData.getStrTimerValue() , 
                                                font = fontTimerLabel,
                                                foreground = self.timerConf.general_conf[ParamCnf.ColorTimerRGB], 
                                                bg=self.timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB] , padx=int(self.timerConf.general_conf[ParamCnf.TimerFontSize]) / 5)
        self.timerData.label.pack()
        
    #modify Font 
    def changeFont(self):  
        self.logger.info('')
        if self.timerData.isActive() == True:
            fontTimerLabel =  tk.font.Font(family=self.timerConf.general_conf[ParamCnf.TimerFontName], weight=self.timerConf.general_conf[ParamCnf.TimerFontStyle], size = int(self.timerConf.general_conf[ParamCnf.TimerFontSize]))
            self.timerData.label.config(font = fontTimerLabel)
     
    
    #modify color timer text 
    def changeFgColorTimer(self):
        self.logger.info('')
        if self.timerConf.general_conf[ParamCnf.ColorTimerRGB] != '':
            self.timerData.label.config( foreground = self.timerConf.general_conf[ParamCnf.ColorTimerRGB])

    #modify color timer text 
    def changeBgColorTimer(self):
        self.logger.info('')
        if self.timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB] != '':
            self.timerData.label.config(bg=self.timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB])
            
    # modify timer value
    def changeValue(self):
        self.timerData.label.config(text = self.timerData.getStrTimerValue())
                                 
    # clean
    def clean(self):
        self.logger.info('')
        if self.timerData.timer != None and self.timerData.timer.is_alive():
            self.timerData.timer.cancel()
        self.timerData.label = None
        
    # setTitle
    def setTitle(self, title):
        self.logger.info('title=%s' % title)
        self.title(title)
        
    # ask before closing application
    def closing_procedure(self, callback, *args, **kwargs):
        self.logger.info('args=%s kwargs=%s' % (args, kwargs))
        if self.mgr.optionsEditorMgr != None:
            tk.messagebox.showwarning('Warning', 'options editor opened, close first', parent=self)
        else:
            self.timerData.timer_conf[ParamTimerCnf.ActiveTimer] = False
            if tk.messagebox.askyesno("Hiding timer", "Do you want the timer to be hidden next time this configuration will be loaded? ", parent = self):
               self.mgr.UTtimerConfig.saveConfiguration()
            self.clean()
            self.mgr.gTimersManager.remove(self)
            callback(*args, **kwargs)
