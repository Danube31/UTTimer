
        #! /usr/bin/env python
# -*- coding: utf-8 -*-
# AbstractGraphicTimerManager: virtual class, handle dynamic and graphical behaviour of Timers 
# 
# 
#  
import tkinter as tk
from TimerData import TimerData
from threading import Timer
from playsound import playsound, PlaysoundException
from Util import *
import pyautogui
from sys import platform
if 'win' in platform:
    import winsound
import logging


class AbstractGraphicTimerManager():
    # constructor
    def __init__(self, mgr):
        self.mgr = mgr;
        self.timerConf = mgr.UTtimerConfig
        
    #modifiy timer status (active/disabled)
    def changeActiveTimer(self, name):
        self.logger.info(' name=%s' % name)
        # recreate labels
        self.mgr.buildGTimers()
        
    #play a sound file
    def playTimerSound(self, sndFile):
        self.logger.info('sndFile=%s' % sndFile)
        if 'win' in platform:
            winsound.PlaySound(sndFile, winsound.SND_ASYNC)
        else:
            try:
                playsound(sndFile, block=False)
            except PlaysoundException:
                self.logger.warning('Can\'t play Audio file: %s' % sndFile)
        
    # return TimerData according to KeyPressed
    def getTimerDataFromKeyPressed(self, KeyPressed):
        self.logger.info('KeyPressed=%s' % KeyPressed)
        for timerData in self.timerConf.TimerDataList:
            if timerData.isActive() == True and timerData.isKeyActive() and KeyPressed == timerData.timer_conf[ParamTimerCnf.TimerKey][0]:
                    return timerData
        return None
            
    # process KeyLog char
    def processKeyChar(self, KeyChar):
        self.logger.info('KeyChar=%s' % KeyChar)
        timerData = self.getTimerDataFromKeyPressed(KeyChar)
        if timerData != None and timerData.isKeyActive()  == True:
            self.launchTimer(timerData)
        elif len(self.timerConf.general_conf[ParamCnf.StartAllTimersKey])==1 and  KeyChar == self.timerConf.general_conf[ParamCnf.StartAllTimersKey][0]:
            self.startAllTimers()
        elif len(self.timerConf.general_conf[ParamCnf.ResetAllTimersKey])==1 and  KeyChar == self.timerConf.general_conf[ParamCnf.ResetAllTimersKey][0]:
            self.resetAllTimers()
            
    # process Key
    def processKeyPressed (self, event):
        self.logger.info('event.char=%s' % event.char)
        self.processKeyChar(event.char)
    
    # Timer management
    def manageTimer(self, timerData):
        self.logger.debug('name=%s' % timerData.timer_conf[ParamTimerCnf.Name])
        timerData.nbSeconds = timerData.nbSeconds - 1
        nbSeconds = timerData.nbSeconds % 60
        nbMinutes = timerData.nbSeconds / 60
        value = "%02d:%02d" % (nbMinutes, nbSeconds)
        timerData.label.config(text = value)
        # timer workflow management
        if timerData.nbSeconds == 0:
            for oTimerData in self.timerConf.TimerDataList:
                if oTimerData != timerData and oTimerData.label != None and oTimerData.nbSeconds == 0:
                    oTimerData.label.config(underline = -1)
            timerData.label.config(fg = self.timerConf.general_conf[ParamCnf.ColorElapsedRGB], underline = 2)
            # GenKey
            if timerData.timer_conf[ParamTimerCnf.ActiveElapsedTimeKey] == True and timerData.timer_conf[ParamTimerCnf.ElapsedTimeKey] != '':
                pyautogui.press(timerData.timer_conf[ParamTimerCnf.ElapsedTimeKey])
                self.logger.debug('ElapsedTime GenKey=%s' % timerData.timer_conf[ParamTimerCnf.ElapsedTimeKey])
        else:
            if timerData.nbSeconds == 1:
                if timerData.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile] != '':
                    self.playTimerSound(timerData.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile] )
            elif timerData.timer_conf[ParamTimerCnf.ThresholdWarning] != '' and timerData.nbSeconds == int(timerData.timer_conf[ParamTimerCnf.ThresholdWarning]) :
                if timerData.timer_conf[ParamTimerCnf.WarningAudioFile]  != '':
                    self.playTimerSound(timerData.timer_conf[ParamTimerCnf.WarningAudioFile] )
                timerData.label.config(fg = self.timerConf.general_conf[ParamCnf.ColorWarningRGB])
                if timerData.timer_conf[ParamTimerCnf.ActiveWarningKey] == True and timerData.timer_conf[ParamTimerCnf.WarningKey] != '':
                    pyautogui.press(timerData.timer_conf[ParamTimerCnf.WarningKey])
                    self.logger.debug('Warning  GenKey=%s' % timerData.timer_conf[ParamTimerCnf.WarningKey])
            timerData.timer = Timer(1, self.manageTimer, [timerData])
            timerData.timer.start()
    
    # launch timer
    def launchTimer(self, timerData, latency = 0):
        self.logger.info('name=%s latency=%d' % (timerData.timer_conf[ParamTimerCnf.Name], latency))
        if self.mgr.optionsEditorMgr == None:
            self.logger.debug('launch timer %s with %d s latency' % (timerData.timer_conf[ParamTimerCnf.Name], latency))
            if timerData.timer != None and timerData.timer.is_alive():
                timerData.timer.cancel()
            if timerData.timer_conf[ParamTimerCnf.StartTimerAudioFile]  != '':
                   self.playTimerSound(timerData.timer_conf[ParamTimerCnf.StartTimerAudioFile] )
            timerData.initTimer(latency)
            timerData.label.config(text = timerData.getStrTimerValue(), fg=self.timerConf.general_conf[ParamCnf.ColorTimerRGB], underline = -1)
            timerData.timer = Timer(1, self.manageTimer, [timerData])
            timerData.timer.start()
            
    # start all timers
    def startAllTimers(self):
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList:
            if timerData.isActive() == True:
                self.launchTimer(timerData)
            
    # reset all timers
    def resetAllTimers(self):
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList:
                if timerData.timer != None and timerData.timer.is_alive():
                    timerData.timer.cancel()
                if timerData.label != None:
                    timerData.label.config(text = timerData.getStrTimerValue(), fg=self.timerConf.general_conf[ParamCnf.ColorTimerRGB], underline=-1)
            
    # speech to command with web latency
    def processSpeech(self, speech, latency):
        self.logger.info('speech=%s latency=%d' % (speech, latency))
        if len(self.timerConf.general_conf['SpeechCommandStartAll']) > 0 and self.timerConf.general_conf['SpeechCommandStartAll'] in speech:
               self.startAllTimers()
        elif len(self.timerConf.general_conf['SpeechCommandResetAll']) > 0 and self.timerConf.general_conf['SpeechCommandResetAll']  in speech:
               self.resetAllTimers()
        else:
            for timerData in self.timerConf.TimerDataList:
                if timerData.isActive() == True  and len(timerData.timer_conf['SpeechCommand']) > 0 and timerData.timer_conf['SpeechCommand'] in speech:
                     self.launchTimer(timerData, latency)
                     break
                                 
    # clean
    def clean(self):
        self.logger.info('')
        for timerData in self.timerConf.TimerDataList:
            if timerData.timer != None and timerData.timer.is_alive():
                timerData.timer.cancel()
        if self.labelNoActiveTimers != None:
            self.labelNoActiveTimers.destroy()
        
    
