#! /usr/bin/env python
# -*- coding: utf-8 -*-
# TimerConfiguration: 
# 
# 
#  
from pathlib import Path
import xml.etree.ElementTree as ET
from TimerData import TimerData
from Util import *
from tkinter import messagebox
import logging

# <configuration>
  # <StartAllTimersKey>6</StartAllTimersKey>
  # <SpeechCommandStartAll>start all</SpeechCommandStartAll>
  # <ResetAllTimersKey>g</ResetAllTimersKey>
  # <SpeechCommandResetAll>reset</SpeechCommandResetAll>
  # <Disposition>True</Disposition>
  # <TimerFontName>System</TimerFontName>
    # <TimerFontSize>80.0</TimerFontSize>
    # <TimerFontStyle>Bold</TimerFontStyle>
  # <ColorTimerRGB> black</ColorTimerRGB>
  # <ColorElapsedRGB>red</ColorElapsedRGB>
  # <ColorWarningRGB>orange</ColorWarningRGB>
  # <Videos>True</Videos>
  # <ExternalKeyLogger>False</ExternalKeyLogger>
  # <KeyLoggerPort>4159</KeyLoggerPort>
 # <ActiveSpeechToCommand>True</ActiveSpeechToCommand>
  # <Language>fr-FR</Language>
  # <Timer name="Armor">
    # <ActiveTimer>True</ActiveTimer>
    # <ColorBackGroundRGB>green</ColorBackGroundRGB>
    # <Minutes>0</Minutes>
    # <Seconds>30</Seconds>
    # <Position>1</Position>
    # <TimerKey>a</TimerKey>
    # <ActiveTimerKey>True</ActiveTimerKey>
    # <ActiveTimerFile>StartArmor.wav</ActiveTimerFile>
    # <ElapsedTimeAudioFile/>
    # <ElapsedTimeKey> </ElapsedTimeKey>
    # <ActiveElapsedTimeKey>False</ActiveElapsedTimeKey>
    # <WarningAudioFile/>
    # <WarningKey> </WarningKey>
    # <ActiveWarningKey>False</ActiveWarningKey>
    # <ThresholdWarning>10</ThresholdWarning>
    # <SpeechCommand>armor taken</SpeechCommand>
  # </Timer>
# </configuration>



# this class loads antenna station data from an  offline file
class TimerConfiguration:       
    
    # XML file containing  default UTTimer parameters (general and timers)
    fileName = 'UTTimerDefaultConfiguration.xml'
    # array of Timer parameters
    TimerDataList = []
    general_conf = {}
    
    # constructor
    def __init__(self, mgr):
        self.mgr = mgr
        self.tree = None
    
    # initialization
    def init(self):
        # main logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('')
        self.initGeneralInformationValues()
    
    # general information initialization
    def initGeneralInformationValues(self):    
        TimerConfiguration.general_conf[ParamCnf.StartAllTimersKey] = ''
        TimerConfiguration.general_conf[ParamCnf.SpeechCommandStartAll]= '' 
        TimerConfiguration.general_conf[ParamCnf.ResetAllTimersKey] = ''
        TimerConfiguration.general_conf[ParamCnf.SpeechCommandResetAll] = ''
        TimerConfiguration.general_conf[ParamCnf.Disposition]= True
        TimerConfiguration.general_conf[ParamCnf.TimerFontName] = 'system'
        TimerConfiguration.general_conf[ParamCnf.TimerFontStyle] = 'bold'
        TimerConfiguration.general_conf[ParamCnf.TimerFontSize] = '80'
        TimerConfiguration.general_conf[ParamCnf.ColorTimerRGB]= '#000000'
        TimerConfiguration.general_conf[ParamCnf.ColorElapsedRGB]= '#FF0000' 
        TimerConfiguration.general_conf[ParamCnf.ColorWarningRGB] = '#FFA500' 
        TimerConfiguration.general_conf[ParamCnf.Videos]= False
        TimerConfiguration.general_conf[ParamCnf.ExternalKeyLogger]= False
        TimerConfiguration.general_conf[ParamCnf.KeyLoggerPort] ='1550'
        TimerConfiguration.general_conf[ParamCnf.ActiveSpeechToCommand] = False
        TimerConfiguration.general_conf[ParamCnf.Language] = 'fr_FR'
        
    # load parameters of XML file
    def load(self):
        self.logger.info('')
        self.tree = ET.parse(self.mgr.cfg_file)
        self.root = self.tree.getroot() 
        # general parameters
        TimerConfiguration.general_conf[ParamCnf.StartAllTimersKey] = getStrNullFromNone(self.root.find(ParamCnf.StartAllTimersKey).text)
        TimerConfiguration.general_conf[ParamCnf.SpeechCommandStartAll]= getStrNullFromNone(self.root.find(ParamCnf.SpeechCommandStartAll).text)
        TimerConfiguration.general_conf[ParamCnf.ResetAllTimersKey] = getStrNullFromNone(self.root.find(ParamCnf.ResetAllTimersKey).text)
        TimerConfiguration.general_conf[ParamCnf.SpeechCommandResetAll] = getStrNullFromNone(self.root.find(ParamCnf.SpeechCommandResetAll).text)
        TimerConfiguration.general_conf[ParamCnf.Disposition]= getStrNullFromNone(self.root.find(ParamCnf.Disposition).text)
        TimerConfiguration.general_conf[ParamCnf.TimerFontName] = getStrNullFromNone(self.root.find(ParamCnf.TimerFontName).text)
        TimerConfiguration.general_conf[ParamCnf.TimerFontStyle] = getStrNullFromNone(self.root.find(ParamCnf.TimerFontStyle).text)
        TimerConfiguration.general_conf[ParamCnf.TimerFontSize] = getStrNullFromNone(self.root.find(ParamCnf.TimerFontSize).text)
        TimerConfiguration.general_conf[ParamCnf.ColorTimerRGB]= getStrNullFromNone(self.root.find(ParamCnf.ColorTimerRGB).text)
        TimerConfiguration.general_conf[ParamCnf.ColorElapsedRGB]= getStrNullFromNone(self.root.find(ParamCnf.ColorElapsedRGB).text)
        TimerConfiguration.general_conf[ParamCnf.ColorWarningRGB] = getStrNullFromNone(self.root.find(ParamCnf.ColorWarningRGB).text)
        TimerConfiguration.general_conf[ParamCnf.Videos]= getBoolFromStr(self.root.find(ParamCnf.Videos).text)
        TimerConfiguration.general_conf[ParamCnf.ExternalKeyLogger]= getBoolFromStr(self.root.find(ParamCnf.ExternalKeyLogger).text)
        TimerConfiguration.general_conf[ParamCnf.KeyLoggerPort] =getStrNullFromNone(self.root.find(ParamCnf.KeyLoggerPort).text)
        TimerConfiguration.general_conf[ParamCnf.ActiveSpeechToCommand] = getBoolFromStr(self.root.find(ParamCnf.ActiveSpeechToCommand).text)
        TimerConfiguration.general_conf[ParamCnf.Language] = getStrNullFromNone(self.root.find(ParamCnf.Language).text)
        # timers parameters
        for count, timerData in enumerate(self.root.findall('Timer')):
            tData = TimerData(count)
            tData.init()
            tData.timer_conf[ParamTimerCnf.Name] = timerData.get(ParamTimerCnf.Name)
            tData.timer_conf[ParamTimerCnf.ActiveTimer] = getBoolFromStr(timerData.find(ParamTimerCnf.ActiveTimer).text)
            tData.timer_conf[ParamTimerCnf.ColorBackGroundRGB] = timerData.find(ParamTimerCnf.ColorBackGroundRGB).text
            if  timerData.find(ParamTimerCnf.Minutes).text == None:
                tData.timer_conf[ParamTimerCnf.MTimerDataListinutes] = '0'
            else:
                tData.timer_conf[ParamTimerCnf.Minutes] = timerData.find(ParamTimerCnf.Minutes).text
            if  timerData.find(ParamTimerCnf.Seconds).text == None:
                tData.timer_conf[ParamTimerCnf.Seconds] = '0'
            else:
                tData.timer_conf[ParamTimerCnf.Seconds] = timerData.find(ParamTimerCnf.Seconds).text
            tData.timer_conf[ParamTimerCnf.Position] = timerData.find(ParamTimerCnf.Position).text
            tData.timer_conf[ParamTimerCnf.TimerKey] = getStrNullFromNone(timerData.find(ParamTimerCnf.TimerKey).text)
            tData.timer_conf[ParamTimerCnf.ActiveTimerKey] = getBoolFromStr(timerData.find(ParamTimerCnf.ActiveTimerKey).text)
            tData.timer_conf[ParamTimerCnf.StartTimerAudioFile] = getStrNullFromNone(timerData.find(ParamTimerCnf.StartTimerAudioFile).text)
            tData.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile] = getStrNullFromNone(timerData.find(ParamTimerCnf.ElapsedTimeAudioFile).text)
            tData.timer_conf[ParamTimerCnf.ElapsedTimeKey] = getStrNullFromNone(timerData.find(ParamTimerCnf.ElapsedTimeKey).text)
            tData.timer_conf[ParamTimerCnf.ActiveElapsedTimeKey] = getBoolFromStr(timerData.find(ParamTimerCnf.ActiveElapsedTimeKey).text)
            tData.timer_conf[ParamTimerCnf.WarningAudioFile] = getStrNullFromNone(timerData.find(ParamTimerCnf.WarningAudioFile).text)
            tData.timer_conf[ParamTimerCnf.WarningKey] = getStrNullFromNone(timerData.find(ParamTimerCnf.WarningKey).text)
            tData.timer_conf[ParamTimerCnf.ActiveWarningKey] = getBoolFromStr(timerData.find(ParamTimerCnf.ActiveWarningKey).text)
            tData.timer_conf[ParamTimerCnf.ThresholdWarning] = getStrNullFromNone(timerData.find(ParamTimerCnf.ThresholdWarning).text)
            tData.timer_conf[ParamTimerCnf.SpeechCommand] = getStrNullFromNone(timerData.find(ParamTimerCnf.SpeechCommand).text)
            TimerConfiguration.TimerDataList.append(tData)
    
    # display configuration parameters
    def print(self):
        self.logger.debug('Configuration dump')
        self.logger.debug("StartAllTimersKey: %s" % TimerConfiguration.general_conf[ParamCnf.StartAllTimersKey])
        self.logger.debug("SpeechCommandStartAll: %s" % TimerConfiguration.general_conf[ParamCnf.SpeechCommandStartAll])
        self.logger.debug("ResetAllTimersKey: %s" % TimerConfiguration.general_conf[ParamCnf.ResetAllTimersKey])
        self.logger.debug("SpeechCommandResetAll: %s" % TimerConfiguration.general_conf[ParamCnf.SpeechCommandResetAll])
        self.logger.debug("Disposition: %s" % TimerConfiguration.general_conf[ParamCnf.Disposition])
        self.logger.debug("TimerFontName: %s" % TimerConfiguration.general_conf[ParamCnf.TimerFontName])
        self.logger.debug("TimerFontSize: %s" % TimerConfiguration.general_conf[ParamCnf.TimerFontSize])
        self.logger.debug("ColorTimerRGB: %s" % TimerConfiguration.general_conf[ParamCnf.TimerFontStyle])
        self.logger.debug("ColorElapsedRGB: %s" % TimerConfiguration.general_conf[ParamCnf.ColorElapsedRGB])
        self.logger.debug("ColorWarningRGB: %s" % TimerConfiguration.general_conf[ParamCnf.ColorWarningRGB])
        self.logger.debug("Videos: %s" % getStrFromBool(TimerConfiguration.general_conf[ParamCnf.Videos]))
        self.logger.debug("ExternalKeyLogger: %s" % getStrFromBool(TimerConfiguration.general_conf[ParamCnf.ExternalKeyLogger]))
        self.logger.debug("KeyLoggerPort: %s" % TimerConfiguration.general_conf[ParamCnf.KeyLoggerPort])
        self.logger.debug("ActiveSpeechCommand: %s" % getStrFromBool(TimerConfiguration.general_conf[ParamCnf.ActiveSpeechToCommand]))
        self.logger.debug("Language: %s" % TimerConfiguration.general_conf[ParamCnf.Language])
        for tData in TimerConfiguration.TimerDataList:
            tData.printConfiguration()
        self.logger.debug('End of Configuration dump')
    
    # save  general information configuration parameters
    def saveGeneralInformation(self):
        self.logger.info('')
        self.root = ET.Element('configuration')
        self.tree = ET.ElementTree(self.root)
        ET.SubElement(self.root, ParamCnf.StartAllTimersKey).text = TimerConfiguration.general_conf[ParamCnf.StartAllTimersKey] 
        ET.SubElement(self.root, ParamCnf.SpeechCommandStartAll).text = TimerConfiguration.general_conf[ParamCnf.SpeechCommandStartAll] 
        ET.SubElement(self.root, ParamCnf.ResetAllTimersKey).text = TimerConfiguration.general_conf[ParamCnf.ResetAllTimersKey] 
        ET.SubElement(self.root, ParamCnf.SpeechCommandResetAll).text = TimerConfiguration.general_conf[ParamCnf.SpeechCommandResetAll] 
        ET.SubElement(self.root, ParamCnf.Disposition).text = TimerConfiguration.general_conf[ParamCnf.Disposition]
        ET.SubElement(self.root, ParamCnf.TimerFontName).text = TimerConfiguration.general_conf[ParamCnf.TimerFontName] 
        ET.SubElement(self.root, ParamCnf.TimerFontStyle).text = TimerConfiguration.general_conf[ParamCnf.TimerFontStyle] 
        ET.SubElement(self.root, ParamCnf.TimerFontSize).text = TimerConfiguration.general_conf[ParamCnf.TimerFontSize] 
        ET.SubElement(self.root, ParamCnf.ColorTimerRGB).text = TimerConfiguration.general_conf[ParamCnf.ColorTimerRGB] 
        ET.SubElement(self.root, ParamCnf.ColorElapsedRGB).text = TimerConfiguration.general_conf[ParamCnf.ColorElapsedRGB] 
        ET.SubElement(self.root, ParamCnf.ColorWarningRGB).text = TimerConfiguration.general_conf[ParamCnf.ColorWarningRGB] 
        ET.SubElement(self.root, ParamCnf.Videos).text = getStrFromBool(TimerConfiguration.general_conf[ParamCnf.Videos])
        ET.SubElement(self.root, ParamCnf.ExternalKeyLogger).text = getStrFromBool(TimerConfiguration.general_conf[ParamCnf.ExternalKeyLogger])
        ET.SubElement(self.root, ParamCnf.KeyLoggerPort).text = TimerConfiguration.general_conf[ParamCnf.KeyLoggerPort]
        ET.SubElement(self.root, ParamCnf.ActiveSpeechToCommand).text = getStrFromBool(TimerConfiguration.general_conf[ParamCnf.ActiveSpeechToCommand])
        ET.SubElement(self.root, ParamCnf.Language).text = TimerConfiguration.general_conf[ParamCnf.Language] 
     
    # save  general information configuration parameters
    def saveTimersInformation(self):
        self.logger.info('')
        for count, timerData in enumerate(TimerConfiguration.TimerDataList):
            timerET = ET.SubElement(self.root, 'Timer')
            timerET.set('Name', timerData.timer_conf[ParamTimerCnf.Name])
            ET.SubElement(timerET, ParamTimerCnf.ActiveTimer).text = getStrFromBool(TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ActiveTimer])
            ET.SubElement(timerET, ParamTimerCnf.ColorBackGroundRGB).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ColorBackGroundRGB] 
            ET.SubElement(timerET, ParamTimerCnf.Minutes).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.Minutes]
            ET.SubElement(timerET, ParamTimerCnf.Seconds).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.Seconds]
            ET.SubElement(timerET, ParamTimerCnf.Position).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.Position] 
            ET.SubElement(timerET, ParamTimerCnf.TimerKey).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.TimerKey] 
            ET.SubElement(timerET, ParamTimerCnf.ActiveTimerKey).text = getStrFromBool(TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ActiveTimerKey])
            ET.SubElement(timerET, ParamTimerCnf.StartTimerAudioFile).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.StartTimerAudioFile] 
            ET.SubElement(timerET, ParamTimerCnf.ElapsedTimeAudioFile).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ElapsedTimeAudioFile] 
            ET.SubElement(timerET, ParamTimerCnf.ElapsedTimeKey).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ElapsedTimeKey] 
            ET.SubElement(timerET, ParamTimerCnf.ActiveElapsedTimeKey).text = getStrFromBool(TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ActiveElapsedTimeKey])
            ET.SubElement(timerET, ParamTimerCnf.WarningAudioFile).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.WarningAudioFile] 
            ET.SubElement(timerET, ParamTimerCnf.WarningKey).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.WarningKey] 
            ET.SubElement(timerET, ParamTimerCnf.ActiveWarningKey).text = getStrFromBool(TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ActiveWarningKey])
            ET.SubElement(timerET, ParamTimerCnf.ThresholdWarning).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.ThresholdWarning] 
            ET.SubElement(timerET, ParamTimerCnf.SpeechCommand).text = TimerConfiguration.TimerDataList[count].timer_conf[ParamTimerCnf.SpeechCommand] 
            
    
    # save to XML
    def saveConfiguration(self, filename = None):
        self.logger.info('%s' % filename)
        # build XML
        self.saveGeneralInformation()
        self.saveTimersInformation()
        # write XML to file
        if filename != None:
            try:
                ET.indent(self.tree, space="\t", level=0)
                #self.dump()
                self.tree.write(filename)
            except PermissionError:
                    messagebox.showerror('OK',  'Configuration file %s can not be written' % filename, parent=self.mgr.optionsEditorMgr)
            self.mgr.cfg_file = filename
        else:
            self.tree.write(self.mgr.cfg_file)
        self.mgr.manageConfigurationFileHistory()
        # list of recent file update
        self.mgr.updateItemsMenuLoadConf()
    
    # debug
    def dump(self):
        self.logger.debug('dump')
        ET.dump(self.root)
                 
    # return TimerData according to Name
    def getTimerDataFromName(self, name):
        self.logger.debug('%s' % name)
        for timerData in self.TimerDataList:
            if name == timerData.timer_conf[ParamTimerCnf.Name]:
                return timerData
        return None
        
    # return TimerData according to Position
    def getTimerDataFromPosition(self, position):
        self.logger.debug('%d' % position)
        for timerData in self.TimerDataList:
            if str(position) == timerData.timer_conf[ParamTimerCnf.Position]:
                return timerData
        return None
        
    # return TimerData according to widget P
    def getTimerDataFromWidget(self, widget):
        self.logger.debug('%s' % widget.__class__.__name__)
        for timerData in self.TimerDataList:
            if widget == timerData.label:
                return timerData
        return None
                
    # clear the list
    def clear(self): 
        self.logger.info('')
        TimerConfiguration.TimerDataList.clear()
        
    # return the list of authorized keys for keylogger
    def getKeysList(self):
        self.logger.info('')
        listKey = []
        for timerData in TimerConfiguration.TimerDataList:
            if timerData.isActive() and timerData.timer_conf[ParamTimerCnf.ActiveTimerKey] == True:
                if len(timerData.timer_conf[ParamTimerCnf.TimerKey]) == 1:
                    listKey.append(timerData.timer_conf[ParamTimerCnf.TimerKey][0])
                
        if len(self.general_conf[ParamCnf.StartAllTimersKey]) == 1:
            listKey.append(self.general_conf[ParamCnf.StartAllTimersKey][0])
    
        if len(self.general_conf[ParamCnf.ResetAllTimersKey]) == 1:
            listKey.append(self.general_conf[ParamCnf.ResetAllTimersKey][0])
            
        strKeysList = ' '.join(listKey)
        self.logger.debug('getKeysList liste=(%s)' %  strKeysList)
        return  strKeysList
        
    # return the list of active timers
    def getActiveTimersList(self):
        self.logger.debug('')
        listActiveTimer=[]
        for timerData in TimerConfiguration.TimerDataList:
            if timerData.isActive():
                listActiveTimer.append(timerData)
        return listActiveTimer
        
    # create new timer
    def createNewTimer(self):
        self.logger.info('')
        timerData = TimerData(len(TimerConfiguration.TimerDataList))
        timerData.init()
        TimerConfiguration.TimerDataList.append(timerData)
        timerData.timer_conf[ParamTimerCnf.Position]=str(len(TimerConfiguration.TimerDataList) - 1)
        return timerData
            
    # remove timer
    def removeTimer(self, timerData):
        self.logger.info('name %s' % timerData.timer_conf[ParamTimerCnf.Name])
        TimerConfiguration.TimerDataList.remove(timerData)
        
    # list lenght
    def getTimerDataListSize(self):
        self.logger.debug('')
        l = len(TimerConfiguration.TimerDataList)
        self.logger.debug('len=%d' % l)
        return l
        
    # new configuration
    def newConfiguration(self):
        self.clear()
        self.initGeneralInformationValues()
        
        
        
    
