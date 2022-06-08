#! /usr/bin/env python
# -*- coding: utf-8 -*-
# DragAndDropManager: handle drag and drop for label timer
# 
# 
#  

from tkinter import *
import tkinter as tk
from  Util import *
import logging

class DragAndDropLabelsManager():
        # constructor
        def __init__(self, gmgr):
                self.gmgr = gmgr
                self.gmgr.bind("<ButtonPress-1>", self.on_start)
                self.gmgr.bind("<B1-Motion>", self.on_drag)
                self.gmgr.bind("<ButtonRelease-1>", self.on_drop)
        
            # initialization
        def init(self):
                # main logger
                self.logger = logging.getLogger(self.__class__.__name__)
                self.logger.info('')
                # update main widget contents  to get final label geometry
                self.gmgr.update()
                # at least one timer and unique size...
                (self.width, self.height)  = self.gmgr.getLabelSize()
                self.logger.debug('timer width=%d, height=%d' % (self.width, self.height))
                self.gmgr.configure(cursor="hand1")
        
        # debug
        def print_geo(self, event):
                return
                self.logger.debug('event.x=%d' % event.x, 'event.y=%d' % event.y)
        
        #left clic down
        def on_start(self, event):
                self.logger.info('')
                self.print_geo(event)
                # offset mouse from top corner of canvas containing moving label
                self.timerData = self.gmgr.timerConf.getTimerDataFromWidget(event.widget)
                self.name = self.timerData.timer_conf[ParamTimerCnf.Name]
                self.logger.debug('name %s' % self.name)
                self.initial_gposition = self.timerData.gposition
                self.gmgr.configure(cursor="hand2")
        
        #drag
        def on_drag(self, event):
                self.logger.debug('')
                self.print_geo(event)
                gposition = self.getPositionFromPointerLocation(event, self.timerData.gposition)
                if self.timerData.gposition != gposition:
                        self.logger.debug('onDrag: %s, previous position %d, new position %d' % (self.name, self.timerData.gposition, gposition))
                        timerDataToMove = self.gmgr.getTimerDataFromGPosition(gposition)
                        timerDataToMove.gposition  = self.timerData.gposition
                        self.timerData.gposition = gposition
                        if int(self.gmgr.timerConf .general_conf[ParamCnf.Disposition]) == TimerDisposition.VERTICAL.value:
                                timerDataToMove.label.grid(row=timerDataToMove.gposition, column=0)
                                self.timerData.label.grid(row=self.timerData.gposition, column=0)
                        else:
                                timerDataToMove.label.grid(row=0, column = timerDataToMove.gposition)
                                self.timerData.label.grid(row=0, column = self.timerData.gposition)
       
        #left clic up
        # eventually save configuration
        def on_drop(self, event):
                self.logger.info('')
                self.print_geo(event)
                if self.timerData.gposition != self.initial_gposition:
                        listPositions = {}
                        for timerData in self.gmgr.timerConf.TimerDataList:
                                if timerData.timer_conf[ParamTimerCnf.ActiveTimer] == True:
                                        listPositions[timerData.timer_conf[ParamTimerCnf.Name]] = timerData.gposition
                                else:
                                        listPositions[timerData.timer_conf[ParamTimerCnf.Name]] = int(timerData.timer_conf[ParamTimerCnf.Position])
                        # recalculte positions
                        listPositions = dict(sorted(listPositions.items(), key=lambda x:x[1]))
                        
                        for timerData in self.gmgr.timerConf.TimerDataList:
                                self.logger.debug('position finale active timer %s: %d' % (timerData.timer_conf[ParamTimerCnf.Name], listPositions[timerData.timer_conf[ParamTimerCnf.Name]]))
                                timerData.timer_conf[ParamTimerCnf.Position] = str(listPositions[timerData.timer_conf[ParamTimerCnf.Name]])
                        # call manager 
                        self.gmgr.onDrop()
                self.gmgr.configure(cursor="hand1")
                
        
        # return position from pointer : in active [1,...,nbTimers]
        def getPositionFromPointerLocation(self, event, gposition):
                self.logger.debug('gposition=%d' % gposition)
                x = event.x
                y = event.y
                nbActiveTimers =  len(self.gmgr.timerConf.getActiveTimersList())
                if  int(self.gmgr.timerConf.general_conf[ParamCnf.Disposition]) == TimerDisposition.VERTICAL.value:
                        yrel = gposition * self.height + y
                        if yrel <=0:
                                position = 0
                        elif yrel >= nbActiveTimers*self.height:
                                position = nbActiveTimers - 1
                        else:
                                position = yrel // self.height
                        self.logger.debug('V : position=%d' % position)
                else:
                        xrel = gposition * self.width + x
                        if xrel <=0:
                                position = 0
                        elif xrel >= nbActiveTimers*self.width:
                                position = nbActiveTimers - 1
                        else:
                                position = xrel // self.width
                        self.logger.debug('H : position=%d' % position)
                return position
                
