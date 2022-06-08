#! /usr/bin/env python
# -*- coding: utf-8 -*-
# TimerConfiguration: 
# 
# 
#  

from Util import *

# <configuration>
  # <Timer Name="Armor">
    # <ColorBackGroundRGB>green</ColorBackGroundRGB>
    # <Minutes>0</Minutes>
    # <Seconds>30</Seconds>
    # <Position>1</Position>
    # <TimerKey>a</TimerKey>
    # <ActiveTimerKey>True</ActiveTimerKey>
    # <StartTimerAudioFile/>
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


		        
class TimerData:
	#constructor
	def __init__(self, index):
		# configuration part
		self.timer_conf = {}
		self.timer_conf[ParamTimerCnf.Name] = "power up %d" % index
		self.timer_conf[ParamTimerCnf.ActiveTimer]  = False
		self.timer_conf[ParamTimerCnf.ColorBackGroundRGB]  = '#FF69B4'
		self.timer_conf[ParamTimerCnf.Minutes] = 2
		self.timer_conf[ParamTimerCnf.Seconds] = 30
		self.timer_conf[ParamTimerCnf.Position]  = 0
		self.timer_conf[ParamTimerCnf.TimerKey]  = ''
		self.timer_conf[ParamTimerCnf.ActiveTimerKey]  = False
		self.timer_conf[ParamTimerCnf.StartTimerAudioFile]  = None
		self.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile]  = None
		self.timer_conf[ParamTimerCnf.ElapsedTimeKey]  = None
		self.timer_conf[ParamTimerCnf.ActiveElapsedTimeKey]  = None
		self.timer_conf[ParamTimerCnf.WarningAudioFile]  = None
		self.timer_conf[ParamTimerCnf.WarningKey]  = None
		self.timer_conf[ParamTimerCnf.ActiveWarningKey]  = None
		self.timer_conf[ParamTimerCnf.ThresholdWarning]  = 10
		self.timer_conf[ParamTimerCnf.SpeechCommand]  = None
		# graphic label
		self.label = None # Label tkinter
		# Timer management
		self.timer = None # timer
		self.gposition = 0
		self.index = index
		
	# initialization
	def init(self):
		# main logger
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.info('')
		self.initTimer()
		
	# display
	def printConfiguration(self):
		self.logger.debug("TimerData")
		self.logger.debug("Name: %s" % self.timer_conf[ParamTimerCnf.Name] ) 
		self.logger.debug("ActiveTimer: %s" % getStrFromBool(self.timer_conf[ParamTimerCnf.ActiveTimer]))
		self.logger.debug("ColorBackGroundRGB: %s" % self.timer_conf[ParamTimerCnf.ColorBackGroundRGB] ) 
		self.logger.debug("Minutes: %s" % str(self.timer_conf[ParamTimerCnf.Minutes])) 
		self.logger.debug("Seconds: %s" % str(self.timer_conf[ParamTimerCnf.Seconds])) 
		self.logger.debug("Position: %s" % str(self.timer_conf[ParamTimerCnf.Position])) 
		self.logger.debug("TimerKey: %s" % self.timer_conf[ParamTimerCnf.TimerKey] ) 
		self.logger.debug("ActiveTimerKey: %s" % getStrFromBool(self.timer_conf[ParamTimerCnf.ActiveTimerKey] ) )
		self.logger.debug("StartTimerAudioFile: %s" % self.timer_conf[ParamTimerCnf.StartTimerAudioFile] ) 
		self.logger.debug("ElapsedTimeAudioFile: %s" % self.timer_conf[ParamTimerCnf.ElapsedTimeAudioFile] ) 
		self.logger.debug("ElapsedTimeKey: %s" % self.timer_conf[ParamTimerCnf.ElapsedTimeKey] ) 
		self.logger.debug("ActiveElapsedTimeKey: %s" % getStrFromBool(self.timer_conf[ParamTimerCnf.ActiveElapsedTimeKey] )) 
		self.logger.debug("WarningAudioFile: %s" % self.timer_conf[ParamTimerCnf.WarningAudioFile] ) 
		self.logger.debug("WarningKey: %s" % self.timer_conf[ParamTimerCnf.WarningKey] ) 
		self.logger.debug("ActiveWarningKey: %s" % getStrFromBool(self.timer_conf[ParamTimerCnf.ActiveWarningKey] )) 
		self.logger.debug("ThresholdWarning: %s" % str(self.timer_conf[ParamTimerCnf.ThresholdWarning])) 
		self.logger.debug("SpeechCommand: %s" % self.timer_conf[ParamTimerCnf.SpeechCommand] ) 
		self.logger.debug("index: %d" % self.index) 
		
	# return True is Timer is active (and display)
	def isActive(self):
		isActive = self.timer_conf[ParamTimerCnf.ActiveTimer]
		self.logger.debug("isActive: %d" % isActive)
		return isActive
		
	# return True is Timer Key is active 
	def isKeyActive(self):
		isKeyActive = self.timer_conf[ParamTimerCnf.ActiveTimerKey] and len(self.timer_conf[ParamTimerCnf.TimerKey]) == 1
		self.logger.debug("isKeyActive: %d", isKeyActive)
		return isKeyActive
		
	# init 
	def initTimer(self, latency = 0):
		self.logger.debug("")
		self.nbSeconds = int(self.timer_conf[ParamTimerCnf.Minutes])*60+int(self.timer_conf[ParamTimerCnf.Seconds]) - latency
	
	# return nb seconds
	def getNbSeconds(self):
		return self.nbSeconds
		
        # return a formatted value "mm:ss"
	def getStrTimerValue(self):
		strTimer = '%02d:%02d' % (int(self.timer_conf[ParamTimerCnf.Minutes]), int(self.timer_conf[ParamTimerCnf.Seconds]))
		self.logger.debug("strTimer: %s" % strTimer)
		return strTimer
		
		
