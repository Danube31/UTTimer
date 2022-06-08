#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Font_wm: handle font selection (found on the net and slightly adapted) 
# 
# 
# 

import tkinter as tk
from tkinter import font
from Util import *
import logging
        

class Font_wm(tk.Toplevel):
        def __init__(self):
                self.running = True
                self.size_min = 10
                self.size_max = 170
                self.result=None

        def init(self, font, title):
                # main logger
                self.logger = logging.getLogger(self.__class__.__name__)
                self.logger.info('')
                tk.Toplevel.__init__(self)
                self.mainfont=font
                self.title(title)
                # Variable
                self.varName=tk.StringVar()# For Font Face
                self.varName.set(self.mainfont.actual('family'))
                self.varSize=tk.StringVar()  # for Font Size
                self.varSize.set(self.mainfont.actual('size'))
                self.varWeight=tk.StringVar() # For Bold
                self.varWeight.set(self.mainfont.actual('weight'))
                # Font Sample
                self.font_1=tk.font.Font()
                for i in ['family', 'weight', 'size']:
                    self.font_1[i]=self.mainfont.actual(i)
                # Main window Frame
                self.mainwindow=tk.Frame(self)
                self.mainwindow.pack(padx=10, pady=10)
                # Main LabelFrame
                self.mainframe=tk.Frame(self.mainwindow)
                self.mainframe.pack(side='top',ipady=30, ipadx=30,expand='no', fill='both')
                self.mainframe0=tk.Frame(self.mainwindow)
                self.mainframe0.pack(side='top', expand='yes', fill='x', padx=10, pady=10)
                self.mainframe1=tk.Frame(self.mainwindow)
                self.mainframe1.pack(side='top',expand='no', fill='both')
                self.mainframe2=tk.Frame(self.mainwindow)
                self.mainframe2.pack(side='top',expand='yes', fill='x', padx=10, pady=10)
                # Frame in [  main frame] list available font names
                self.frameName=tk.LabelFrame(self.mainframe, text='Select Font Name')
                self.frameName.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
                self.frameSize=tk.LabelFrame(self.mainframe, text='Select Font size')
                self.frameSize.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
                tk.Entry(self.frameName, textvariable=self.varName).pack(side='top', padx=5, pady=5, expand='yes', fill='x')
                self.listbox=tk.Listbox(self.frameName, bg='gray70')
                self.listbox.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
                # linux platform noto color emoji font cause an X error, leave it...
                for i in sorted(set(tk.font.families())):
                    self.listbox.insert(tk.END, i)
                # Frame in [ 0. mainframe] => weight
                self.bold=tk.Checkbutton(self.mainframe0, text='Bold', onvalue='bold', offvalue='normal', variable=self.varWeight)
                self.bold.pack(side='left',expand='yes', fill='x')
                # Frame in [ 1. main frame] => size
                self.sizeScale = tk.Scale(self.frameSize, variable = self.varSize, from_ = self.size_max, to = self.size_min, tickinterval = 10, command = self.checksize)
                self.sizeScale.pack(side='top', padx=5, pady=5, expand='yes', fill='y')
                #windows
                self.sizeScale.bind('<MouseWheel>', self.sizeWheel)
                #linux
                self.sizeScale.bind('<Button-4>', self.sizeWheel)
                self.sizeScale.bind('<Button-5>', self.sizeWheel)
                tk.Label(self.mainframe1, bg='white',text='01:30', font=self.font_1).pack(expand='no', padx=10,pady=10)
                # Frame in [ 2. mainframe] buttons
                tk.Button(self.mainframe2, text=' Cancel ', command=self.end).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
                tk.Button(self.mainframe2, text='   OK   ', command=self.out).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
                
                self.listbox.bind('<<ListboxSelect>>', self.checkface)

        # Function
        def checkface(self, event):
            self.logger.info('')
            try:
                self.varName.set(str(self.listbox.get(self.listbox.curselection())))
                self.font_1.config(family=self.varName.get(), size=self.varSize.get(), weight=self.varWeight.get())
            except:
               pass
               
        def checksize(self, event):
            self.logger.debug('')
            try:
                self.varSize.set(self.sizeScale.get())
                self.font_1.config(family=self.varName.get(), size=self.varSize.get(), weight=self.varWeight.get())
            except:
                pass           
            
        def out(self):
            self.logger.info('')
            self.result=(self.varName.get(), self.varSize.get(), self.varWeight.get())
            self.mainfont['family']=self.varName.get()
            self.mainfont['size']=int(self.varSize.get())
            self.mainfont['weight']=self.varWeight.get()
            self.destroy()
            self.running = False
            
        def end(self):
            self.logger.info('')
            self.destroy()
            
        def sizeWheel(self , event):
                self.logger.debug('')
                if event.num == 5 or event.delta < 0:
                        step = -1
                else:
                        step = 1
                step += int(self.varSize.get())
                if step >= self.size_min and  step <= self.size_max:
                        self.varSize.set(str(step)) 
                        self.checksize(event)           
                            
        # to get the font
        def askFont(font, title):
                chooser = Font_wm()
                chooser.init(font, title)
                chooser.wait_window(chooser)
                return chooser.result
                
