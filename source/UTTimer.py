#! /usr/bin/env python
# -*- coding: utf-8 -*-
# UTTimer: main program with UT Timer manager
# provides timers to manage powerup (Udam, Belt, Armor, Big health, Missile, etc) 
# timer may be triggered by application keystroke, from an external keylogger or by speech to text command
# UTTimer work flow
# 1/ the main manager  eventually loads an XML configuration file if given through argument
# 2/ it prepares speech recognition if required in configuration file (SpeechToCommand)
# 3/ it builds GUI and instanciates the class in charge of graphical and behaviour properties ( GraphicTimersManager)


import sys
from optparse import OptionParser
from UTTimerManager import UTTimerManager
from sys import platform
from Util import *
import colorama
import logging
import tkinter as tk
     
# main procedure
if __name__ == '__main__':
    # print colors init (for win32)
    colorama.init()
    # parse args   
    usage = 'python3 %s [-c|--conf <configuration file> -l|--log <DEBUG|INFO|WARNING] -f|--file <log file> -x|--xsd <xsd file>]' % (sys.argv[0])
    parser = OptionParser(usage)
    parser.add_option("-c", "--conf",
                      action="store", type="string", dest="cfg_file",
                      help="optionnal, configuration file")
    parser.add_option("-l", "--log",
                      action="store", type="string", dest="log_level",
                      help="optional, logging option; DEBUG|INFO|WARNING, ERROR and CRITICAL are logged by default ")
    parser.add_option("-f", "--file",
                      action="store", type="string", dest="log_file",
                      help="optionnal, file logging")
    parser.add_option("-x", "--xsd",
                      action="store", type="string", dest="xsd_file",
                      help="optionnal, xsd validation schema")
    (options, args) = parser.parse_args()
    kwargs = {}
    if options.log_level != None:
        if  options.log_level  in logging_pattern.keys():
            logLevel = logging_pattern[options.log_level]
        else:
            print('option log is not correct %s' % getColoredStr(options.log_level, 'red'))
            print(usage)
            sys.exit(-1)
        kwargs['level'] = logLevel
        kwargs['format'] = '%(asctime)s  - %(levelname)8s - %(name)s - line %(lineno)d - %(funcName)s  - %(message)s'
        kwargs['datefmt'] = '%m/%d/%Y %H:%M:%S'
    if options.log_file != None:
        if  options.log_level == None:
            print('no option level log, default ERROR and CRITICAL' )
        else:
            kwargs['filename'] = options.log_file
    else:
            print('no file log, default stdout' )
    # logging configuration
    logging.basicConfig(**kwargs)
    logger = logging.getLogger('main')
    # log platform
    logger.info('UTTimer running on %s platform' % platform)
    # create manager
    UTTimerMgr =  UTTimerManager(platform)
    # init manager
    UTTimerMgr.init()
    # 1/ XML configuration file management
    if options.cfg_file != None:
        logger.info('configuration file %s' % options.cfg_file)
        UTTimerMgr.checkFile(options.cfg_file, options.xsd_file)
        UTTimerMgr.loadFile(options.cfg_file)
        fileToOpen = options.cfg_file
    else:
        logger.info('no configuration file')
        fileToOpen = None
    # 2/ if set up, the manager prepare speech to text command
    UTTimerMgr.prepareSpeechToCommand()
    # 3/ manager builds GUI 
    UTTimerMgr.buildGUI(fileToOpen != None)
    
    # for logger in logging.root.manager.loggerDict:
        # print("logger name : %s" % logger)
    # mainloop
    UTTimerMgr.mainloop()
            
            
    
    
    
