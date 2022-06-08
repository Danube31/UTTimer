#! /usr/bin/env python
# -*- coding: utf-8 -*-
# LabelDemoUT: specialize tkinter Label behaviour
# 
# 
#  
from tkinter import *
import tkinter as tk
from threading import Timer, Thread
from Util import *
import logging

class LabelDemoUT(Label):
    def __init__(self, master, omgr):
        super().__init__(master)
        self.omgr = omgr
        self.indexTimer = 0
        self.index = 0
        self.timer = None
        self.freeze = False
        
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.launchTimer()
        
         # Timer management
    def manageTimer(self):
        self.logger.debug('')
        nbTimers = self.omgr.timerConf.getTimerDataListSize()
        if nbTimers > 0: 
            if self.freeze == False:
                timerData = self.omgr.timerConf.TimerDataList[self.index]
                timerData.nbSeconds -=  1
                nbSeconds = timerData.nbSeconds % 60
                nbMinutes = timerData.nbSeconds / 60
                value = "%02d:%02d" % (nbMinutes, nbSeconds)
                self.config(text = value)
                if timerData.nbSeconds == 0:
                    self.config(fg = self.omgr.generalInformationTab.Var[ParamCnf.ColorElapsedRGB].var.get(), underline = 2)
                    self.indexTimer += 1
                    self.timer = Timer(3, self.launchTimer)
                    self.timer.start()
                else:
                    if timerData.timer_conf[ParamTimerCnf.ThresholdWarning] != '' and timerData.nbSeconds == int(timerData.timer_conf[ParamTimerCnf.ThresholdWarning]):
                        self.config(fg = self.omgr.generalInformationTab.Var[ParamCnf.ColorWarningRGB].var.get())
                    self.timer = Timer(1, self.manageTimer)
                    self.timer.start()
            else:
                    self.timer = Timer(1, self.manageTimer)
                    self.timer.start()
            
    
    # launch timer
    def launchTimer(self):
        self.logger.info('')
        nbTimers = self.omgr.timerConf.getTimerDataListSize()
        if nbTimers > 0: 
            self.clean()
            self.index = self.indexTimer % nbTimers
            timerData = self.omgr.timerConf.TimerDataList[self.index]
            timerData.initTimer()
            self.config(text=timerData.getStrTimerValue(), 
                                foreground= self.omgr.generalInformationTab.Var[ParamCnf.ColorTimerRGB].var.get(), 
                                bg = timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB], 
                                font = self.omgr.generalInformationTab.getVarTimerFont(), underline = -1)
            self.timer = Timer(1, self.manageTimer)
            self.timer.start()
        else:
            self.config(text="13:37", 
                                foreground= self.omgr.generalInformationTab.Var[ParamCnf.ColorTimerRGB].var.get(), 
                                font = self.omgr.generalInformationTab.getVarTimerFont(), underline = -1)
        
    # clean
    def clean(self):
        self.logger.info('')
        if self.timer != None:
            self.timer.cancel()
            
    # freeze
    def freeZe(self):
        self.freeze = True

    # unfreeze
    def unfreeZe(self):
        self.freeze = False
    
  
