#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SpeechToCommand: handle speech to command (recognition) 
#  based on SpeechRecognition python module (needs pyaudio)
# 
#  
import speech_recognition as sr
from threading import Thread
import time
from datetime import datetime, timedelta
from math import floor
import logging

class SpeechToCommand:

    activated = False
             
    # constructor
    def __init__(self):
        sr.Microphone(device_index = 0)
        print(f"MICs Found on this Computer: \n {sr.Microphone.list_microphone_names()}")
        # Creating a recognition object
        self.r = sr.Recognizer()
        self.r.energy_threshold=4000
        self.r.dynamic_energy_threshold = False
        
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        
    # activation of speech to command
    def activateSpeechToCommand(self, graphicTimerMgr):
        self.logger.info('graphicTimerMgr=%s' % graphicTimerMgr.__class__.__name__)
        if SpeechToCommand.activated == False:
                self.graphicTimerMgr = graphicTimerMgr
                # thread processing speech
                self.loop = True
                self.threadDetectSpeechCommand = Thread(target = self.fn_speech_recognition)
                self.threadDetectSpeechCommand.daemon = True
                self.threadDetectSpeechCommand.start() 
                SpeechToCommand.activated = True

    # callback for thread
    def fn_speech_recognition(self):
        self.logger.info('')
        while self.loop:
            with sr.Microphone() as source:
                self.logger.debug('Please Speak Loud and Clear:')
                #reduce noise
                self.r.adjust_for_ambient_noise(source)
                try:
                    #take voice input from the microphone
                    audio = self.r.listen(source)
                    dateaudio = datetime.now()
                except sr.WaitTimeoutError:
                    self.logger.error("listening timed out while waiting for phrase to start")
                else:
                    try:
                        # google is your international friend
                        speech = self.r.recognize_google(audio, language=self.graphicTimerMgr.timerConf.general_conf['Language'])
                        latency = (datetime.now() - dateaudio).total_seconds()
                        self.logger.debug('recognize: %s with %f s latency' % (speech, latency))
                        # process speech with the latency
                        latency = 0
                        self.graphicTimerMgr.processSpeech(speech, floor(latency))
                    except sr.UnknownValueError as msg:
                        if msg != None:
                            self.logger.error(msg)
                    except sr.RequestError as msg:
                        if msg != None:
                            self.logger.error(msg)
                        
    # to kill speech recognition thread (may take a while to properly kill the thread) 
    def clean(self):
        self.logger.info('')
        self.loop = False
        

