#! /usr/bin/env python
# -*- coding: utf-8 -*-
# InfoTab: Virtual class
# 
# 
#  

from tkinter.colorchooser import askcolor
from Util import *


class DataVarTab:
        # constructor
        def __init__(self, var, applyFunc, *args, **kwargs):
                self.var = var
                self.applyFunc = applyFunc
                self.args = args
                self.kwargs = kwargs
        

class AbstractInfoTab:
        # constructor
        def __init__(self, omgr, frame):
                self.omgr = omgr
                self.frame = frame
                self.timerConf = omgr.timerConf 
                self.isModified = False
                self.Var = {} 
        
        # pick color
        def pickColorAndApply(self, str_var_key, title, label, typeGround):
                colors = askcolor(title = title, color = self.Var[str_var_key].var.get(), parent = self.omgr)
                if colors != (None, None):
                        self.Var[str_var_key].var.set(colors[1])
                        if typeGround == ParamGroundType.fg:
                                label.config(foreground=colors[1])
                        else:
                                label.config(bg=colors[1])
