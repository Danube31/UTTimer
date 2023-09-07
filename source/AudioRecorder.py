#! /usr/bin/env python
# -*- coding: utf-8 -*-
# AudioRecorder: Widget managing recording (ElapsedTime and Warning audio)
# 
# 
#  


import tkinter as tk
from tkinter import ttk
from Util import *
import logging
import pyaudio
import wave
import time
import os
from threading import Thread
import audioop

class AudioRecorder(tk.Toplevel):
     # constructor
    def __init__(self, omgr):
        super().__init__(omgr)
        self.omgr = omgr
        # Record in chunks of 1024 samples
        self.chunk = 1024 
        # 16 bits per sample
        self.sample_format = pyaudio.paInt16 
        self.channels = 2
        # Record at 44400 samples per second
        self.smpl_rt = 44400 
        self.result = None
        self.maxAudioMeter = 32768
    
    def init(self, title):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        # Create an interface to PortAudio
        self.pa = pyaudio.PyAudio() 
        
        self.title('Recording tool for ' + title)
        # 1/ Timer frame
        RecordFrame = tk.LabelFrame(self, text = 'Record')
        RecordFrame.pack(fill = 'x')
        
        labelInputAudioDevice = tk.Label(RecordFrame, text = 'Input audio device: ')
        labelInputAudioDevice.grid(row = 0, column = 0)
        listInputAudioDevice = []
        indexMaxInputChannels = 1
        maxInputChannels = 0
        lengthInputAudioDeviceName  = 0
        #load effective audio device to populate combobox
        for i in range(self.pa.get_device_count()):
            dev = self.pa.get_device_info_by_index(i)
            nbChannels = dev['maxInputChannels']
            self.logger.debug('audio device name %s nb channels=%d' % (dev['name'], nbChannels))
            if  nbChannels > 0 and nbChannels < 64:
                if len(dev['name']) > lengthInputAudioDeviceName:
                    lengthInputAudioDeviceName = len(dev['name'])
                listInputAudioDevice.append(dev['name'])
                if nbChannels > maxInputChannels:
                    maxInputChannels = nbChannels 
                    indexMaxInputChannels  = i
        
        self.logger.info(' choosing input channels=%d, input=%s' % (maxInputChannels, self.pa.get_device_info_by_index(indexMaxInputChannels)['name']))
        # input audio devices combobox 
        self.comboInputAudioDevice = ttk.Combobox(RecordFrame, width=lengthInputAudioDeviceName, values=listInputAudioDevice)
        self.comboInputAudioDevice.grid(row = 0, column = 1)
        self.comboInputAudioDevice.current(indexMaxInputChannels)
        self.channels = maxInputChannels
 
        global img # bug PhotoImage
        img = tk.PhotoImage(file=self.omgr.mgr.get_absfile('resources/StartRecord.png'))
        self.buttonRecord = tk.Button(RecordFrame, image=img, command=self.record)
        self.buttonRecord.grid(row = 1, column = 0)    
        
        global img1# bug PhotoImage...
        img1 = tk.PhotoImage(file=self.omgr.mgr.get_absfile('resources/StopRecord.png'))
        self.buttonStop = tk.Button(RecordFrame, image=img1, command=self.stopRecording, state=tk.DISABLED)
        self.buttonStop.grid(row = 1, column = 1)    
            
        self.buttonSave = tk.Button(RecordFrame, text='Save', command= self.pickFileAndSave, state=tk.DISABLED)
        self.buttonSave.grid(row = 1, column = 2)       
        
        self.audioMeter = ttk.Progressbar(RecordFrame, mode = 'determinate', orient = tk.HORIZONTAL, length=150)
        self.audioMeter.grid(row = 2, column = 0)    
        
        labelAudioFile= tk.Label(RecordFrame, text = 'Audio file: ')
        labelAudioFile.grid(row = 3, column = 0)       
        
        self.labelAudioInfo= tk.Label(RecordFrame, text = '                                                                                                          ')
        self.labelAudioInfo.grid(row = 3, column = 1)
        
        self.buttonCancel = tk.Button(self, text="Cancel", command=lambda : self.closing_procedure(False, self.destroy))
        self.buttonCancel.pack(padx=10, pady=10, side= 'left' )
        
        self.buttonOK = tk.Button(self, text="OK", command=lambda : self.closing_procedure(True, self.destroy))
        self.buttonOK.pack(padx=10, pady=10, side= 'right' )
        
        # close the window with X
        self.protocol("WM_DELETE_WINDOW", lambda : self.closing_procedure(self.destroy))
                
    # record     
    def record(self):
        self.logger.info('')
        self.buttonRecord.config(state = tk.DISABLED)
        self.buttonSave.config(state = tk.DISABLED)
        self.buttonStop.config(state = tk.NORMAL)
        self.labelAudioInfo.config(text='Recording...')
        self.input_device_index =  self.comboInputAudioDevice.current()
        self.channels = self.pa.get_device_info_by_index(self.input_device_index)['maxInputChannels']
        self.logger.info('Recording channels=%d, input=%s' % (self.channels, self.pa.get_device_info_by_index(self.input_device_index)['name']))
        self.buttonCancel.config(state = tk.DISABLED)
        self.buttonOK.config(state = tk.DISABLED)
        self.recording = True
        recordThread = Thread(target=self.threadRecord)
        recordThread.daemon = True
        recordThread.start()
         
    # stop recording
    def stopRecording(self):
        self.logger.info('')
        self.buttonRecord.config(state = tk.NORMAL)
        self.buttonStop.config(state = tk.DISABLED)
        self.recording = False
        self.labelAudioInfo.config(text='End of recording')
        self.buttonSave.config(state = tk.NORMAL)
        self.buttonCancel.config(state = tk.NORMAL)
        self.buttonOK.config(state = tk.NORMAL)
        
     #pick/new conf file and save
    def pickFileAndSave(self):
        self.logger.info('')
        filename = tk.filedialog.asksaveasfilename(title='Wav audio file chooser', initialdir = os.getcwd(), filetypes=(("wav files", "*.wav"),), parent = self)
        if filename:
            self.logger.info(filename)
            # Save the recorded data in a .wav format
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pa.get_sample_size(self.sample_format))
            wf.setframerate(self.smpl_rt)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            self.result = filename
            self.labelAudioInfo.config(text='Recorded to %s' % filename)
            self.buttonSave.config(state = tk.DISABLED)
    
    # exception raised
    def processException(self, msg):
        self.logger.warning(msg)
        self.labelAudioInfo.config(text=msg)
        self.recording =  False
        self.buttonRecord.config(state = tk.NORMAL)
        self.buttonStop.config(state = tk.DISABLED)
        self.buttonCancel.config(state = tk.NORMAL)
        self.buttonOK.config(state = tk.NORMAL)
        
    # record thread
    def threadRecord(self):
        self.logger.info('')
        try:
            stream = self.pa.open(format=self.sample_format, 
                             channels=self.channels,
                             rate=self.smpl_rt, 
                             input=True, 
                             input_device_index = self.input_device_index,
                             frames_per_buffer=self.chunk)
        except OSError as msg:
            self.processException(msg)
        except ValueError as msg:
            self.processException(msg)
        else:                   
            # Initialize array that will be used for storing 
            self.frames = [] 
            while self.recording == True:
                try:
                    data = stream.read(self.chunk)
                except OSError as msg:
                    txt = msg + ' Device %s unavailable for recording' % self.pa.get_device_info_by_index(self.input_device_index)['name']
                    self.processException(txt)
                else:           
                    self.audioMeter['value'] = int(audioop.max(data, 2)*100/self.maxAudioMeter) 
                    self.frames.append(data)
                    # Stop and close the stream
            stream.stop_stream()
            stream.close()
        
    # clean before closing application
    def closing_procedure(self, result, callback, *args, **kwargs):
        if result == False:
            self.result = None
        self.recording = False
        self.pa.terminate()
        callback(*args, **kwargs)
        
  # to get the audio file
    def askAudioFile(title, omgr):
            chooser = AudioRecorder(omgr)
            chooser.init(title)
            chooser.wait_window(chooser)
            return chooser.result   
