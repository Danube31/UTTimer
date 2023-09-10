#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Util: useful classes
# 
# 
#  

from enum import Enum
import locale
from sys import platform
from colorama import Fore, Style
import logging

class ParamCnf():
        StartAllTimersKey = 'StartAllTimersKey'
        SpeechCommandStartAll = 'SpeechCommandStartAll'
        ResetAllTimersKey = 'ResetAllTimersKey'
        SpeechCommandResetAll = 'SpeechCommandResetAll'
        Disposition = 'Disposition'
        TimerFontName = 'TimerFontName'
        TimerFontStyle = 'TimerFontStyle'
        TimerFontSize = 'TimerFontSize'
        ColorTimerRGB = 'ColorTimerRGB'
        ColorElapsedRGB = 'ColorElapsedRGB'
        ColorWarningRGB = 'ColorWarningRGB'
        Videos = 'Videos'
        InternalKeyLogger = 'InternalKeyLogger'
        ActiveSpeechToCommand = 'ActiveSpeechToCommand'
        Language = 'Language'
                
class ParamTimerCnf():
        Name = 'Name'
        ActiveTimer = 'ActiveTimer'
        ColorBackGroundRGB = 'ColorBackGroundRGB'
        Minutes = 'Minutes'
        Seconds = 'Seconds'
        Position = 'Position'
        TimerKey = 'TimerKey'
        ActiveTimerKey = 'ActiveTimerKey'
        StartTimerAudioFile = 'StartTimerAudioFile'
        ElapsedTimeAudioFile = 'ElapsedTimeAudioFile'
        ElapsedTimeKey = 'ElapsedTimeKey'
        ActiveElapsedTimeKey = 'ActiveElapsedTimeKey'
        WarningAudioFile = 'WarningAudioFile'
        WarningKey = 'WarningKey'
        ActiveWarningKey = 'ActiveWarningKey'
        ThresholdWarning = 'ThresholdWarning'
        InternalKeyLogger = 'InternalKeyLogger'
        SpeechCommand = 'SpeechCommand'
        
if "win" in platform:
        class SelectFile():
                AUDIOFILES = (("wav files", "*.wav"),) 
                XMLFILES = (('xml files', '*.xml'),) 
else:
        class SelectFile():
                AUDIOFILES = (("m4a files", "*.m4a"), ("wav files", "*.wav"), ("mp3 files", "*.mp3")) 
                XMLFILES = (('xml files', '*.xml'),) 

class ParamStatus(Enum):
        NONMODIFIED = 0
        MODIFIED = 1
        APPLIED = 2
        SAVED = 3


class TimerDisposition(Enum):
        DETACHED = 0
        VERTICAL = 1
        HORIZONTAL = 2
            
class ParamGroundType(Enum):
        fg = 0
        bg = 1
        
# get string 'True'/'False' from boolean
def getStrFromBool(b):
    s = None
    if b == True:
        s = 'true'
    else:
        s = 'false'
    return s
        
# get  boolean from string 'True'/'False'
def getBoolFromStr(s):
    b = None
    if s == 'true':
        b = True
    elif s == 'false' :
        b = False
    return b
    
    
# get str null from None
def getStrNullFromNone(s):
    sr = ''
    if s != None:
        sr = s
    return sr

# strip locale
def stripMap(loc):
        tab = loc.split('.')
        return tab[0]
        
# get list of language from locale (depending upon platform
def getListofLanguagesFromLocale():
        if "win" in platform:
                listOfLanguage = list(set(map(stripMap, locale.windows_locale.values())))
        else:
                listOfLanguage = list(set(map(stripMap, locale.locale_alias.values())))
        for lang in listOfLanguage.copy():
                if len(lang) != 5 or lang[2] != '_':
                        listOfLanguage.remove(lang)
        return sorted(listOfLanguage)
        
# class limiting Entry string lenght input 
class VarStrLimiter:
    def __init__(self, str_var, length):
        self.length = length
        str_var.trace("w", lambda name, index, mode, str_var=str_var: self.callback(str_var))
        
    def callback(self, str_var):
        c = str_var.get()[0:self.length]
        str_var.set(c)
        
# class limiting Entry integer range input 
class VarRangeIntegerLimiter:
    def __init__(self, str_var, _min, _max):
        self._min = _min
        self._max = _max
        str_var.trace("w", lambda name, index, mode, str_var=str_var: self.callback(str_var))
        
    def callback(self, str_var):
                try:
                        c = str_var.get()
                except:
                        c = str(self._min)
                if  (int(c) >= self._min and int(c) <= self._max) :
                        str_var.set(c)
        
# limit integer for Entry tkinter (validate command)
class IntegerLimitedEntr:
        def __init__(self, master):
                self.master = master
        
        # check integer only 
        def  integerValidation(self, P):
                return P.isdigit()
                        
        def getValidateCommand(self):
                return (self.master.register(self.integerValidation),'%P')

# limit integer range for Entry tkinter (validate command)
class   RangeIntegerLimitedEntry:
        def __init__(self, master, m, M, func = None):
                self.master = master
                self.min = m
                self.max = M
                self.func = func
                
        # check integer only within range
        def  integerMinMaxValidation(self, P):
                return P == '' or (P.isdigit() and int(P) >= self.min and int(P)<=self.max)
                        
        def getValidateCommand(self):
                return (self.master.register(self.integerMinMaxValidation),'%P')
 
# limit str size for Entry tkinter (validate command)               
class   LengthStrLimitedEntry:
        def __init__(self, master, length):
                self.master = master
                self.length = length
                
        # check integer only within range
        def  lengthValidation(self, P):
                return (len(P)<=self.length)
                        
        def getValidateCommand(self):
                return (self.master.register(self.lengthValidation),'%P')
                
# colored code for print
color_msg = {'blue': Fore.BLUE,
                 'green': Fore.GREEN,
                 'yellow': Fore.YELLOW,
                 'red': Fore.RED,
                 'black': Fore.BLACK,
                 'white': Fore.WHITE}

# get colored code for print
def getColoredStr(msg, color):
        return color_msg[color] + msg + Style.RESET_ALL
        
# logging pattern
logging_pattern = {'DEBUG': logging.DEBUG,
                 'INFO': logging.INFO,
                 'WARNING': logging.WARNING}
