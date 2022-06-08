#! /usr/bin/env python
# -*- coding: utf-8 -*-
# GraphicDetachedTimerManager: handle detached Timers 
# 
# 
#  
from TimerData import TimerData
from Util import *
import logging
from GraphicDetachedTimer import GraphicDetachedTimer
from AbstractGraphicTimerManager import AbstractGraphicTimerManager


class GraphicDetachedTimersManager(AbstractGraphicTimerManager):
    # constructor
    def __init__(self, mgr):
        super().__init__(mgr)
        
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.graphicDetachedTimersList = []
        self.createLabelTimers()
  
    # (re)create Labels
    def createLabelTimers(self):
        self.logger.info('')
        for timerData in self.mgr.UTtimerConfig.TimerDataList:    
            if timerData.isActive() == True:
                if timerData.label != None:
                    timerData.label.destroy()
                    timerData.label = None
                graphicDetachedTimer = GraphicDetachedTimer(self.mgr, timerData.timer_conf[ParamTimerCnf.Name])
                graphicDetachedTimer.init()
                self.graphicDetachedTimersList.append(graphicDetachedTimer)
                
    #modifiy Disposition
    def changeDisposition(self):
        self.logger.info('')
        if int(self.timerConf.general_conf[ParamCnf.Disposition]) != TimerDisposition.DETACHED.value:
            for graphicDetachedTimer in self.graphicDetachedTimersList: 
                graphicDetachedTimer.clean()
                graphicDetachedTimer.destroy()
            self.graphicDetachedTimersList.clear()
            self.mgr.buildGTimers()
        
    #modify Font 
    def changeFont(self):  
        self.logger.info('')
        for graphicDetachedTimer in self.graphicDetachedTimersList: 
            graphicDetachedTimer.changeFont()
    
    #modify color timer text 
    def changeFgColorTimer(self):
        self.logger.info('')
        for graphicDetachedTimer in self.graphicDetachedTimersList: 
            graphicDetachedTimer.changeFgColorTimer()
    
    #modify color timer text 
    def changeBgColorTimer(self, name):
        self.logger.info(' name=%s' % name)
        for graphicDetachedTimer in self.graphicDetachedTimersList: 
            if graphicDetachedTimer.timerData.timer_conf[ParamTimerCnf.Name] == name:
                graphicDetachedTimer.changeBgColorTimer()
                
    #modify timer value
    def changeValue(self, name):
        self.logger.info(' name=%s' % name)
        for graphicDetachedTimer in self.graphicDetachedTimersList: 
            if graphicDetachedTimer.timerData.timer_conf[ParamTimerCnf.Name] == name:
                graphicDetachedTimer.changeValue()

    #modifiy timer status (active/disabled)
    def changeActiveTimer(self, name):
        self.logger.info(' name=%s' % name)
        # recreate labels
        self.mgr.buildGTimers()
        
    #on remove timer
    def removeTimer(self):
        self.logger.info('')
        # TBD
                         
    # clean
    def clean(self):
        self.logger.info('')
        for graphicDetachedTimer in self.graphicDetachedTimersList:
            graphicDetachedTimer.clean()

    # destroy
    def destroy(self):
        self.logger.info('')
        for graphicDetachedTimer in self.graphicDetachedTimersList: 
            graphicDetachedTimer.clean()
            graphicDetachedTimer.destroy()
        self.graphicDetachedTimersList.clear()
        
    # remove graphicDetachedTimer from the graphic detached timers list
    def remove(self, graphicDetachedTimer):
        self.graphicDetachedTimersList.remove(graphicDetachedTimer)
    
