#! /usr/bin/env python
# -*- coding: utf-8 -*-
# AudioFileWidget: handle audio file management
# 
# 
#  
import tkinter as tk
from Util import *
import logging
import os

class AudioFileWidget:
    
    # constructor
    def __init__(self):
        pass
        
    # initialization
    def init(self, title, timerTab, frame, audioFileTag, audioFile, row):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')

        # label may display audio file
        tk.Label(frame, text='Audio file: ').grid(row = row, column = 0)
        
        # Audio
        if audioFile != None  and audioFile != '':
            textLabel = os.path.basename(audioFile)
        else:
            textLabel = SelectFile.AUDIOFILES
            
        # label may display audio file
        self.labelAudioFile= tk.Label(frame, text=textLabel)
        self.labelAudioFile.grid(row = row, column = 1)
    
        # button to pick audio file 
        self.buttonPickFile = tk.Button(frame, text="Browse...")
        self.buttonPickFile.grid(row = row, column = 2, padx=5)
        
        # button to play audio file 
        self.buttonPlayAudioFile = tk.Button(frame, text="Play", command= lambda : timerTab.playAudioFile(audioFileTag))
        self.buttonPlayAudioFile.grid(row = row, column = 3)
        
        # button to remove audio file 
        self.buttonRemoveAudioFile = tk.Button(frame, text="Remove")
        self.buttonRemoveAudioFile.grid(row = row, column = 4)
        
        # button to record audio file 
        self.buttonRecordAudioFile = tk.Button(frame, text="Record")
        self.buttonRecordAudioFile.grid(row = row, column = 5, padx=15)
        
        if  textLabel == SelectFile.AUDIOFILES:
                self.buttonPlayAudioFile.config(state=tk.DISABLED)
                self.buttonRemoveAudioFile.config(state=tk.DISABLED)
        
        # command attached to buttons
        self.buttonPickFile.config(command = lambda : timerTab.pickFileAndApply(audioFileTag,'%s Audio File Picker' % audioFileTag, self.labelAudioFile,  self.buttonPlayAudioFile, self.buttonRemoveAudioFile))
        self.buttonRemoveAudioFile.config(command = lambda : timerTab.removeAudioFile(audioFileTag, self.labelAudioFile,  self.buttonPlayAudioFile, self.buttonRemoveAudioFile))
        self.buttonRecordAudioFile.config(command = lambda : timerTab.recordAudioFile(audioFileTag, title, self.labelAudioFile,  self.buttonPlayAudioFile, self.buttonRemoveAudioFile, self.buttonRecordAudioFile))
        
