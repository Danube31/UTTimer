#! /usr/bin/env python
# -*- coding: utf-8 -*-
# TimerTab: handle Timer information tab of OptionsEditorManager
# 
# 
#  
import tkinter as tk
from TimerData import TimerData
from Util import *
from InfoTab import *
from os import path
from tkinter import filedialog
from playsound import playsound
from tkinter import messagebox
from AudioRecorder import AudioRecorder
from AudioFileWidget import AudioFileWidget

        
        
# class building timer tab
class TimerTab(AbstractInfoTab):
    
    NOFILESELECTED = 'no audio file selected'
     
    # constructor
    def __init__(self, omgr, frame, name):
        super().__init__(omgr, frame)
        self.name = name
        self.timerData = self.timerConf.getTimerDataFromName(self.name)
        # Var/Func initialization
        self.Var[ParamTimerCnf.Name] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.Name]), self.omgr.changeName, self.name)
        self.Var[ParamTimerCnf.ActiveTimer] = DataVarTab(tk.BooleanVar(value = self.timerData.timer_conf[ParamTimerCnf.ActiveTimer]), self.omgr.changeActiveTimer, self.name)
        self.Var[ParamTimerCnf.TimerKey] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.TimerKey]), None)
        self.Var[ParamTimerCnf.ActiveTimerKey] = DataVarTab(tk.BooleanVar(value = self.timerData.timer_conf[ParamTimerCnf.ActiveTimerKey]), None)
        self.Var[ParamTimerCnf.StartTimerAudioFile] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.StartTimerAudioFile]), None)
        self.Var[ParamTimerCnf.Minutes] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.Minutes]), self.omgr.changeValue, self.name)
        self.Var[ParamTimerCnf.Seconds] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.Seconds]),  self.omgr.changeValue, self.name)
        self.Var[ParamTimerCnf.ColorBackGroundRGB] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB]), self.omgr.changeBgColorTimer, self.name)
        self.Var[ParamTimerCnf.ElapsedTimeAudioFile] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile]), None)
        self.Var[ParamTimerCnf.ElapsedTimeKey] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.ElapsedTimeKey]), None)
        self.Var[ParamTimerCnf.ActiveElapsedTimeKey] = DataVarTab(tk.BooleanVar(value = self.timerData.timer_conf[ParamTimerCnf.ActiveElapsedTimeKey]), None)
        self.Var[ParamTimerCnf.WarningAudioFile] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.WarningAudioFile]), None)
        self.Var[ParamTimerCnf.WarningKey] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.WarningKey]), None)
        self.Var[ParamTimerCnf.ActiveWarningKey] = DataVarTab(tk.BooleanVar(value = self.timerData.timer_conf[ParamTimerCnf.ActiveWarningKey]), None)
        self.Var[ParamTimerCnf.ThresholdWarning] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.ThresholdWarning]), None)
        self.Var[ParamTimerCnf.SpeechCommand] = DataVarTab(tk.StringVar(value = self.timerData.timer_conf[ParamTimerCnf.SpeechCommand]), None)
        
        # modification detection
        for key in self.Var.keys():
                self.Var[key].var.trace_add('write', self.omgr.configurationModified)
            
        
    # init HMI
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        
        # 1/ Timer frame
        TimerFrame= tk.LabelFrame(self.frame, text = 'Timer')
        TimerFrame.pack(fill = 'x')
        
        labelTimerDisplay = tk.Label(TimerFrame, text = 'Active: ')
        labelTimerDisplay.grid(row = 0, column = 0)
        
        self.activeTimerCheckButton = tk.Checkbutton(TimerFrame, variable=self.Var[ParamTimerCnf.ActiveTimer].var)
        self.activeTimerCheckButton.grid(row=0, column=1)
        
        labelTimerName = tk.Label(TimerFrame, text = 'Name: ')
        labelTimerName.grid(row = 0, column = 2)
        
        self.TimerNameEntry = tk.Entry(TimerFrame, width=10, textvariable=self.Var[ParamTimerCnf.Name].var  )
        self.TimerNameEntry.grid(row = 0, column = 3)
        
        # button to remove timer
        self.buttonRemoveTimer = tk.Button(TimerFrame, text="Remove timer", command=self.removeTimer)
        self.buttonRemoveTimer.grid(row = 0, column = 4, padx=50)
        
        # 2/ key frame
        KeyFrame= tk.LabelFrame(self.frame, text = 'Key')
        KeyFrame.pack(fill = 'x')
        
        labelActiveTimerKey = tk.Label(KeyFrame, text = 'Active Key: ')
        labelActiveTimerKey.grid(row = 0, column = 0)
        
        activeTimerKeyCheckButton = tk.Checkbutton(KeyFrame, variable=self.Var[ParamTimerCnf.ActiveTimerKey].var)
        activeTimerKeyCheckButton.grid(row=0, column=1)
        
        labelTimerKey = tk.Label(KeyFrame, text = '   Key: ')
        labelTimerKey.grid(row = 0, column = 2)
        
        vmcd = LengthStrLimitedEntry( KeyFrame, 1)
        self.keyEntry = tk.Entry(KeyFrame, width=1, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamTimerCnf.TimerKey].var  )
        self.keyEntry.grid(row = 0, column = 3)
        
        # Audio file
        startTimerAudioFileWidget = AudioFileWidget()
        startTimerAudioFileWidget.init('Start', self, KeyFrame, ParamTimerCnf.StartTimerAudioFile, self.timerData.timer_conf[ParamTimerCnf.StartTimerAudioFile], 1)   
             
       # 3/ Duration Frame
        DurationFrame= tk.LabelFrame(self.frame, text = 'Duration')
        DurationFrame.pack(fill = 'x')
        
        labelDuration1= tk.Label(DurationFrame, text = 'Timer duration (mm:ss) : ')
        labelDuration1.grid(row = 0, column = 0)
        
        vmcd = RangeIntegerLimitedEntry( DurationFrame, 0, 60)
        self.minutesEntry = tk.Entry(DurationFrame, width=2, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamTimerCnf.Minutes].var  )
        self.minutesEntry.grid(row = 0, column = 1)
        
        labelDuration2= tk.Label(DurationFrame, text = ' : ')
        labelDuration2.grid(row = 0, column = 2)
        
        vmcd = RangeIntegerLimitedEntry( DurationFrame , 0, 60)
        self.secondsEntry = tk.Entry(DurationFrame, width=2, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamTimerCnf.Seconds].var  )
        self.secondsEntry.grid(row = 0, column = 3)
        
        # 4/ Background Color frame
        BackGroundColorFrame= tk.LabelFrame(self.frame, text = 'Background color')
        BackGroundColorFrame.pack(fill = 'x')
        
        textLabel = '    '+self.getStrTimerValue()+'    '
        self.labelBgColor= tk.Label(BackGroundColorFrame, text=textLabel, bg = self.timerData.timer_conf[ParamTimerCnf.ColorBackGroundRGB])
        self.labelBgColor.grid(row = 0, column = 0)

        # button to pick backgroung color 
        self.buttonBgColor = tk.Button(BackGroundColorFrame, text="Color...", command= lambda : self.pickColorAndApply(ParamTimerCnf.ColorBackGroundRGB, 'Background Color Picker', self.labelBgColor, ParamGroundType.bg))
        self.buttonBgColor.grid(row = 0, column = 1)
        
        # 5/ Elapsed Time frame
        ElapsedTimeFrame= tk.LabelFrame(self.frame, text = 'Elapsed Time')
        ElapsedTimeFrame.pack(fill = 'x')
        
        # Audio file
        elapsedTimerAudioFileWidget = AudioFileWidget()
        elapsedTimerAudioFileWidget.init('Elapsed timer', self, ElapsedTimeFrame, ParamTimerCnf.ElapsedTimeAudioFile, self.timerData.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile], 0)
        
        # key gen
        labelElapsedTimeKey1 = tk.Label(ElapsedTimeFrame, text = 'Enable gen key: ')
        labelElapsedTimeKey1.grid(row = 1, column = 0)
        
        activeElapsedTimeKeyCheckButton = tk.Checkbutton(ElapsedTimeFrame, variable=self.Var[ParamTimerCnf.ActiveElapsedTimeKey].var)
        activeElapsedTimeKeyCheckButton.grid(row=1, column=1)
         
        labelElapsedTimerKey2 = tk.Label(ElapsedTimeFrame, text = '  Gen key: ')
        labelElapsedTimerKey2.grid(row = 1, column = 2)
        
        vmcd = LengthStrLimitedEntry( ElapsedTimeFrame, 1)
        self.elapsedTimeKeyEntry = tk.Entry(ElapsedTimeFrame, width=1, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamTimerCnf.ElapsedTimeKey].var  )
        self.elapsedTimeKeyEntry.grid(row = 1, column = 3)

        # 6/ Warning frame
        WarningFrame= tk.LabelFrame(self.frame, text = 'Warning')
        WarningFrame.pack(fill = 'x')
    
        # Audio file
        warningAudioFileWidget = AudioFileWidget()
        warningAudioFileWidget.init('Warning', self, WarningFrame, ParamTimerCnf.WarningAudioFile, self.timerData.timer_conf[ParamTimerCnf.WarningAudioFile], 0)
             
        # key gen
        labelWarningKey1 = tk.Label(WarningFrame, text = 'Enable gen key: ')
        labelWarningKey1.grid(row = 1, column = 0)
        
        activeWarningKeyCheckButton = tk.Checkbutton(WarningFrame, variable=self.Var[ParamTimerCnf.ActiveWarningKey].var)
        activeWarningKeyCheckButton.grid(row=1, column=1)
         
        labelWarningKey2 = tk.Label(WarningFrame, text = '  Gen key: ')
        labelWarningKey2.grid(row = 1, column = 2)
        
        vmcd = LengthStrLimitedEntry( ElapsedTimeFrame, 1)
        self.warningKeyEntry = tk.Entry(WarningFrame, width=1, validate='key', validatecommand= vmcd.getValidateCommand(), textvariable=self.Var[ParamTimerCnf.WarningKey].var  )
        self.warningKeyEntry.grid(row = 1, column = 3)
  
        labelThresholdWarning= tk.Label(WarningFrame, text = 'Threshold warning (s) : ')
        labelThresholdWarning.grid(row = 2, column = 0)
        
        maxVal = int(self.Var[ParamTimerCnf.Minutes].var.get())*60+ int(self.Var[ParamTimerCnf.Seconds].var.get()) - 1
         
        vmcd = RangeIntegerLimitedEntry(WarningFrame, 0, maxVal)
        self.thresholdWarningEntry = tk.Entry(WarningFrame, width=10, validate='key', validatecommand= vmcd.getValidateCommand())
        self.thresholdWarningEntry['textvariable'] = self.Var[ParamTimerCnf.ThresholdWarning].var
        self.thresholdWarningEntry.grid(row = 2, column = 1)      
           
        # Speech to command
        
        # 7/ Speech recognized command
        SpeechCommandFrame= tk.LabelFrame(self.frame, text='Speech to command')
        SpeechCommandFrame.pack(fill = 'x', expand=True)
        
        tk.Label(SpeechCommandFrame, text = 'command: ').grid(row = 0, column = 0)
        
        self.SpeechCommandEntry = tk.Entry(SpeechCommandFrame, width=10,  textvariable=self.Var[ParamTimerCnf.SpeechCommand].var  )
        self.SpeechCommandEntry.grid(row = 0, column = 1)
        
   
     # bind
    def bind(self):    
        self.logger.info('') 
        # to manage modifications
        #self.frame.bind("<Enter>", self.isTimerConfModified)
        #self.frame.bind("<Leave>", self.isTimerConfModified)
                 
    # pick color for timer background
    def pickColor(self, str_var_key, title, label):
        super().pickColor(str_var_key, title, label)
        self.logger.info('str_var_key=%s title=%s label.text=%s'% (str_var_key, title, label.__class__.__name__))
        if str_var_key == ParamTimerCnf.ColorBackGroundRGB:
            self.labelBgColor.config(bg=self.Var[str_var_key].var.get())
                
    #pick audio file
    def pickFileAndApply(self, str_var_key, title, label, buttonPlay, buttonRemove):
        self.logger.info('str_var_key=%s title=%s, label.text=%s'% (str_var_key, title, label.__class__.__name__))
        filename = filedialog.askopenfilename(initialdir = '.', title=title, filetypes=SelectFile.AUDIOFILES, parent = self.omgr)
        if filename:
            self.Var[str_var_key].var.set(filename)
            label.config(text=path.basename(filename))
            buttonPlay.config(state=tk.NORMAL)
            buttonRemove.config(state=tk.NORMAL)
      
    #play audio file      
    def playAudioFile(self, str_var_key):
        self.logger.info('str_var_key=%s'% str_var_key)
        self.omgr.mgr.gTimersManager.playTimerSound(self.Var[str_var_key].var.get())
        
    #remove audio file      
    def removeAudioFile(self, str_var_key, label, buttonPlay, buttonRemove):
        self.logger.info('str_var_key=%s '% str_var_key)
        self.Var[str_var_key].var.set('')
        label.config(text=SelectFile.AUDIOFILES)
        buttonPlay.config(state=tk.DISABLED)
        buttonRemove.config(state=tk.DISABLED)
    
    #remove audio file      
    def recordAudioFile(self, str_var_key, title, label, buttonPlay, buttonRemove, buttonRecord):
        self.logger.info('str_var_key=%s' % str_var_key)
        buttonRecord.config(state=tk.DISABLED)
        # record tool
        audioFile = AudioRecorder.askAudioFile(title, self.omgr)
        self.logger.info('audio file=%s' % audioFile)
        if audioFile:
                self.Var[str_var_key].var.set(audioFile)
                label.config(text=path.basename(audioFile))
                buttonPlay.config(state=tk.NORMAL)
                buttonRemove.config(state=tk.NORMAL)
        buttonRecord.config(state=tk.NORMAL)
                    
    # check if at least one general parameter has been modified
    def isTimerConfModified(self):
        self.logger.debug('')
        isModified = False
        for key in self.Var.keys():
            timerData = self.timerConf.getTimerDataFromName(self.name)
            if self.Var[key].var.get() != timerData.timer_conf[key]:
                self.logger.debug('conf modified key %s' % key)
                isModified = True
                break;
        return (isModified)
    
    # apply  modifications to XML
    def applyConfigurationChanges(self):
        self.logger.info('')
        timerData = self.timerConf.getTimerDataFromName(self.name)
        for key in self.Var.keys():
                if timerData.timer_conf[key] != self.Var[key].var.get():
                        timerData.timer_conf[key] = self.Var[key].var.get()
                        if self.Var[key].applyFunc != None:
                                self.Var[key].applyFunc(*self.Var[key].args, **self.Var[key].kwargs)
             
    
    # return a formatted value "mm:ss"
    def getStrTimerValue(self):
        strHHMM = '%02d:%02d' % (int(self.Var[ParamTimerCnf.Minutes].var.get()), int(self.Var[ParamTimerCnf.Seconds].var.get()))
        self.logger.debug('getStrTimerValue HH:MM=%s '% strHHMM)
        return strHHMM
        
    # clean
    def clean(self):
        self.logger.info('')
        pass
        
    # remove timer
    def removeTimer(self):
        self.logger.info('')
        if messagebox.askyesno("Remove Timer", "Do you really want to remove %s timer ? " % self.name, parent = self.omgr):
            self.logger.debug('remove timer %s' % self.name)
            self.omgr.removeTimer(self.name)

    # check if empty timer var name
    def timerNameVarLenght(self):
        self.logger.debug('lenght %s : %d' % (self.Var[ParamTimerCnf.Name].var.get(), len(self.Var[ParamTimerCnf.Name].var.get())))
        return len(self.Var[ParamTimerCnf.Name].var.get())

