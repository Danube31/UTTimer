#! /usr/bin/env python
# -*- coding: utf-8 -*-
# GeneralInformationTab: handle general information tab of OptionsEditorManager
# 
# 
#  
import tkinter as tk
from TimerData import TimerData
from FontChooser import Font_wm
from Util import *
from InfoTab import *
from tkinter import font
from LabelDemoUT import LabelDemoUT
import logging

# class building general information tab
class GeneralInformationTab(AbstractInfoTab):
    # constructor
        def __init__(self, omgr, frame):
                super().__init__(omgr, frame)
                
                # Var/Func initialization
                self.Var[ParamCnf.StartAllTimersKey]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.StartAllTimersKey]), None)
                self.Var[ParamCnf.SpeechCommandStartAll]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.SpeechCommandStartAll]), None)
                self.Var[ParamCnf.ResetAllTimersKey]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.ResetAllTimersKey]), None)
                self.Var[ParamCnf.SpeechCommandResetAll]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.SpeechCommandResetAll]), None)
                self.Var[ParamCnf.ColorTimerRGB] = DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.ColorTimerRGB]), self.omgr.changeFgColorTimer)
                self.Var[ParamCnf.ColorWarningRGB] = DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.ColorWarningRGB]), None)
                self.Var[ParamCnf.ColorElapsedRGB] = DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.ColorElapsedRGB]), None)
                self.Var[ParamCnf.Disposition]  = DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.Disposition]), self.omgr.changeDisposition)
                self.Var[ParamCnf.TimerFontName] = DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.TimerFontName]), self.omgr.changeFont)
                self.Var[ParamCnf.TimerFontStyle]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.TimerFontStyle]), self.omgr.changeFont)
                self.Var[ParamCnf.TimerFontSize]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.TimerFontSize]), self.omgr.changeFont)
                self.Var[ParamCnf.ActiveSpeechToCommand]= DataVarTab(tk.BooleanVar(value = self.timerConf.general_conf[ParamCnf.ActiveSpeechToCommand]), None)
                self.Var[ParamCnf.Language]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.Language]), None)
                self.Var[ParamCnf.KeyLoggerPort]= DataVarTab(tk.StringVar(value = self.timerConf.general_conf[ParamCnf.KeyLoggerPort]), None)
                self.Var[ParamCnf.InternalKeyLogger]= DataVarTab(tk.BooleanVar(value = self.timerConf.general_conf[ParamCnf.InternalKeyLogger]), self.omgr.changeInternalKeyLogger)
                self.Var[ParamCnf.Videos]= DataVarTab(tk.BooleanVar(value = self.timerConf.general_conf[ParamCnf.Videos]), None)
                
                # modification detection
                for key in self.Var.keys():
                        self.Var[key].var.trace_add('write', self.omgr.configurationModified)

        # init tab content
        def init(self):
                # main logger
                self.logger = logging.getLogger(self.__class__.__name__)
                self.logger.info('')
                
                # 1/ General keys frame
                generalKeysFrame= tk.LabelFrame(self.frame, text='General keys')
                generalKeysFrame.pack(fill = 'x')
                
                labelStartAllTimersKey = tk.Label(generalKeysFrame, text = 'start all timers key: ')
                labelStartAllTimersKey.grid(row = 0, column = 0)
                
                vmcd = LengthStrLimitedEntry(generalKeysFrame, 1)
                self.startAllTimersEntry = tk.Entry(generalKeysFrame, width=1, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamCnf.StartAllTimersKey].var)
                self.startAllTimersEntry.grid(row = 0, column = 1)
                
                labelResetAllTimersKey = tk.Label(generalKeysFrame, text = '  reset all timers key: ')
                labelResetAllTimersKey.grid(row = 0, column = 2)
                
                vmcd = LengthStrLimitedEntry(generalKeysFrame , 1)
                self.resetAllTimersEntry = tk.Entry(generalKeysFrame, width=1, validate='key', validatecommand= vmcd.getValidateCommand(), textvariable= self.Var[ParamCnf.ResetAllTimersKey].var)
                self.resetAllTimersEntry.grid(row = 0, column = 3)
            
                # 2/ General colors
                generalColorsFrame= tk.LabelFrame(self.frame, text='General colors')
                generalColorsFrame.pack(fill = 'x', expand=True)
                
                #label Timer color
                labelTimerColor = tk.Label(generalColorsFrame, text = 'Timer color: ', foreground = self.timerConf.general_conf[ParamCnf.ColorTimerRGB])
                labelTimerColor.grid(row = 0, column = 0)
                
                # button to pick Timer color 
                self.buttonTimerColor = tk.Button(generalColorsFrame, text="Color...", command= lambda : self.pickColorAndApply(ParamCnf.ColorTimerRGB, 'Timer Color Picker', labelTimerColor, ParamGroundType.fg))
                self.buttonTimerColor.grid(row = 0, column = 1)
                
                #label warning color
                labelWarningColor = tk.Label(generalColorsFrame, text = '   Warning color: ', foreground = self.timerConf.general_conf[ParamCnf.ColorWarningRGB])
                labelWarningColor.grid(row = 0, column = 2)
                
                # button to pick Warning color 
                self.buttonWarningColor = tk.Button(generalColorsFrame, text="Color...", command= lambda : self.pickColorAndApply(ParamCnf.ColorWarningRGB, 'Warning Color Picker', labelWarningColor, ParamGroundType.fg))
                self.buttonWarningColor.grid(row = 0, column = 3)
                
                #label elapsed color
                labelElapsedColor = tk.Label(generalColorsFrame, text = '   Elapsed color: ', foreground = self.timerConf.general_conf[ParamCnf.ColorElapsedRGB])
                labelElapsedColor.grid(row = 0, column = 4)
                
                # button to pick Elapsed color 
                self.buttonElapsedColor = tk.Button(generalColorsFrame, text="Color...", command= lambda : self.pickColorAndApply(ParamCnf.ColorElapsedRGB, 'Elapsed Color Picker', labelElapsedColor, ParamGroundType.fg))
                self.buttonElapsedColor.grid(row = 0, column = 5)
                
                # 3/ Timers alignement
                generalTimersDispositionFrame= tk.LabelFrame(self.frame, text='Timers Disposition')
                generalTimersDispositionFrame.pack(fill = 'x', expand=True)
                
                tk.Label(generalTimersDispositionFrame, text = 'Detached').grid(row=0, column=0)
                DetachedRadioButton = tk.Radiobutton(generalTimersDispositionFrame, variable=self.Var[ParamCnf.Disposition].var , value = '0')
                DetachedRadioButton.grid(row=1, column=0)
                tk.Label(generalTimersDispositionFrame, text = 'Vertical').grid(row=0, column=1, padx = 10)
                VerticalRadioButton = tk.Radiobutton(generalTimersDispositionFrame, variable=self.Var[ParamCnf.Disposition].var , value = '1')
                VerticalRadioButton.grid(row=1, column=1, padx = 10)
                tk.Label(generalTimersDispositionFrame, text = 'Horizontal').grid(row=0, column=2, padx = 10)
                HorizontalRadioButton = tk.Radiobutton(generalTimersDispositionFrame, variable=self.Var[ParamCnf.Disposition].var , value = '2')
                HorizontalRadioButton.grid(row=1, column=2, padx = 10)
                
                
                # 4/ Font selector
                generalFontFrame= tk.LabelFrame(self.frame, text='Timers Font')
                generalFontFrame.pack(fill = 'x', expand=True)
                
                self.labelTimeFontName = tk.Label(generalFontFrame, textvariable=self.Var[ParamCnf.TimerFontName].var)
                self.labelTimeFontName.pack(side='left')
                
                self.labelTimeFontStyle = tk.Label(generalFontFrame, textvariable=self.Var[ParamCnf.TimerFontStyle].var)
                self.labelTimeFontStyle.pack(side='left')
                
                tk.Label(generalFontFrame, text = ', size: ').pack(side='left')
                
                self.labelTimeFontSize = tk.Label(generalFontFrame, textvariable=self.Var[ParamCnf.TimerFontSize].var)
                self.labelTimeFontSize.pack(side='left')
                
                self.buttonFont = tk.Button(generalFontFrame, text="Font...", command= lambda : self.chooseFont())
                self.buttonFont.pack(side='left')

                self.textFontDemo = LabelDemoUT(generalFontFrame, self.omgr)
                self.textFontDemo.init()
                self.textFontDemo.pack()
                
                
                # 6/ Speech recognized command
                SpeechCommandFrame= tk.LabelFrame(self.frame, text='Speech to command')
                SpeechCommandFrame.pack(fill = 'x', expand=True)
                
                tk.Label(SpeechCommandFrame, text = '  Active Speech to command: ').grid(row = 0, column = 0)
                
                activeSpeechToCommandCheckButton = tk.Checkbutton(SpeechCommandFrame, variable=self.Var[ParamCnf.ActiveSpeechToCommand].var)
                activeSpeechToCommandCheckButton.grid(row=0, column=1)
                
                tk.Label(SpeechCommandFrame, text = 'Language: ').grid(row = 0, column = 2)
                
                languageComboxBox = tk.ttk.Combobox(SpeechCommandFrame, textvariable=self.Var[ParamCnf.Language].var)
                listLanguages = getListofLanguagesFromLocale()
                languageComboxBox['value'] = listLanguages
                languageComboxBox['state'] = 'readonly'
                languageComboxBox.grid(row=0, column=3)
                
                tk.Label(SpeechCommandFrame, text = 'Start all timers command: ').grid(row = 1, column = 0)
                
                self.SpeechCommandStartAllEntry = tk.Entry(SpeechCommandFrame, width=10,  textvariable=self.Var[ParamCnf.SpeechCommandStartAll].var  )
                self.SpeechCommandStartAllEntry.grid(row = 1, column = 1)
                
                
                tk.Label(SpeechCommandFrame, text = ' Reset all timers command: ').grid(row = 1, column = 2)
                
                self.SpeechCommandResetAllEntry = tk.Entry(SpeechCommandFrame, width=10,  textvariable=self.Var[ParamCnf.SpeechCommandResetAll].var  )
                self.SpeechCommandResetAllEntry.grid(row = 1, column = 3)
                
            
                
                # 7/ Miscellaneous
                miscellaneousFrame= tk.LabelFrame(self.frame, text='Miscellaneous')
                miscellaneousFrame.pack(fill = 'x', expand=True)
                
                tk.Label(miscellaneousFrame, text = 'Internal Keylogger: ').grid(row = 0, column = 0)
                
                InternalKeyLoggerCheckButton = tk.Checkbutton(miscellaneousFrame, variable=self.Var[ParamCnf.InternalKeyLogger].var)
                InternalKeyLoggerCheckButton.grid(row=0, column=1)
                
                tk.Label(miscellaneousFrame, text = 'Internal Keylogger port: ').grid(row = 0, column = 2, padx=20)
                
                vmcd = RangeIntegerLimitedEntry(miscellaneousFrame , 0, 9999)
                self.keyLoggerPortEntry = tk.Entry(miscellaneousFrame, width=4, validate='key', validatecommand= vmcd.getValidateCommand(),  textvariable=self.Var[ParamCnf.KeyLoggerPort].var  )
                self.keyLoggerPortEntry.grid(row = 0, column = 3)
                
                
        # bind
        def bind(self):
                self.logger.info('')
        
        # pick color for timer foreground
        def pickColorAndApply(self, str_var_key, title, label, typeGround):
                super().pickColorAndApply(str_var_key, title, label, typeGround)
                self.logger.info('str_var_key=%s title=%s label=%s typeGround=%d' % (str_var_key, title, label.__class__.__name__, typeGround.value))
                if str_var_key == ParamCnf.ColorTimerRGB:
                        self.textFontDemo.config(foreground=self.Var[str_var_key].var.get())
    
    
        # choose Font for timer foreground
        def chooseFont(self):
                self.logger.info('')
                font_modified = Font_wm.askFont(tk.font.Font(family = self.Var[ParamCnf.TimerFontName].var.get(), weight = self.Var[ParamCnf.TimerFontStyle].var.get(), size = self.Var[ParamCnf.TimerFontSize].var.get()), 'Timer Font...')
                if font_modified != None:
                        self.Var[ParamCnf.TimerFontName].var.set(font_modified[0])
                        self.Var[ParamCnf.TimerFontSize].var.set(font_modified[1])
                        self.Var[ParamCnf.TimerFontStyle].var.set(font_modified[2])
                        self.textFontDemo.config(font = self.getVarTimerFont())
    
        # get TimerFont from conf variable
        def getTimerFont(self):
                self.logger.info('')
                return font.Font(family=self.timerConf.general_conf[ParamCnf.TimerFontName], weight=self.timerConf.general_conf[ParamCnf.TimerFontStyle] , size=int(self.timerConf.general_conf[ParamCnf.TimerFontSize]))
     
        # get TimerFont from options variable       
        def getVarTimerFont(self):
                self.logger.info('')
                return font.Font(family=self.Var[ParamCnf.TimerFontName].var.get(), weight=self.Var[ParamCnf.TimerFontStyle].var.get() , size=int(self.Var[ParamCnf.TimerFontSize].var.get()))
            
        # check if at least one general parameter has been modified
        def isGeneralInfoConfModified(self):
                self.logger.debug('')
                isModified =  False
                for key in self.Var.keys():
                    if self.Var[key].var.get() != self.timerConf.general_conf[key]:
                        self.logger.debug('conf modified key %s' % key)
                        isModified = True
                        break;
                return isModified
        
        # apply  modifications to XML
        def applyConfigurationChanges(self):
                self.logger.info('')
                for key in self.Var.keys():
                        if self.timerConf.general_conf[key] != self.Var[key].var.get():
                                self.timerConf.general_conf[key] = self.Var[key].var.get()
                                if self.Var[key].applyFunc != None:
                                        self.Var[key].applyFunc(*self.Var[key].args, **self.Var[key].kwargs)
             
        
        # clean before destroy
        def clean(self):
                self.logger.info('')
                self.textFontDemo.clean()
                
        def update(self):
                self.logger.info('')
                self.textFontDemo.launchTimer()
