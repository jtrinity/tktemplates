# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 14:07:57 2016

@author: Jesse Trinity (Coleman Lab)
"""

import Tkinter as tk
import tkFileDialog
import numpy as np
import csv as csv

#-----WIDGETS-----
#Generic window framework
class Window(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.bind("<FocusIn>", self.parent.on_focus_in)
        
        if ('title' in kwargs):
            self.title(kwargs['title'])
            
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    #kill root when this window is closed
    def on_closing(self):
        self.parent.destroy()
        

#Generic *gridded* button framework
class Button(tk.Button):
    def __init__(self, container, name, command, position):
        button = tk.Button(container, text = name, command = command)
        button.grid(row = position[0], column = position[1], padx = 5, pady  = 5, sticky = tk.N+tk.S+tk.E+tk.W)
        
     
#-----Main Application-----
class MainApp(tk.Tk):
    def __init__(self, master = None, *args, **kwargs):
        tk.Tk.__init__(self, master, *args, **kwargs)
        self.title("Main Window")
        
        #populate windows by (class, name)
        self.windows = dict()
        for (C, n) in ((window_one, "window 1"), (window_two,"window 2")):
            window = C(self, title = n)
            self.windows[C] = window
        
        self.bind("<FocusIn>", self.on_focus_in)
                
        #create windows by name
#        window_names = ("window1", "window2")
#        windows = {name:Window(self.root, title = name) for name in window_names}
               
        #-----class widgets-----
        #labels
        self.title_frame= tk.Frame(self)
        self.title_frame.pack(side = "top")
        
        self.title_label = tk.Label(self.title_frame, text = "Toolbar")
        self.title_label.grid(row = 0, column = 0)
        
        #Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side = "top")
        
        self.load_button = Button(self.button_frame, "load file", self.load, (1,0))
                
        self.button1 = Button(self.button_frame, "button 1", self.default_onclick, (1,1))
        
        self.button2 = Button(self.button_frame, "button 2", self.default_onclick, (1,2))
        
        self.button3 = Button(self.button_frame, "button 3", self.default_onclick, (1,3))
        
        #-----end widgets-----
        
        #variables
        self.file_list = list()
        self.data = list()
        
        #set root window position (needs to happen last to account for widget sizes)
        self.update()
        self.hpos =  self.winfo_screenwidth()/2 - self.winfo_width()/2
        self.vpos = 0
        self.geometry("+%d+%d" % (self.hpos, self.vpos))
        
        self.mainloop()
    
    #Dummy command function
    def default_onclick(self):
        print "widget pressed"
    
    #Dummy event function
    def default_on_event(self):
        print "event detected"
        
    def on_focus_in(self, event):
        self.lift()
        for win in self.windows:
            self.windows[win].lift()
    
    #Open a file dialog and record selected filenames to self.file_names
    def load(self):
        files = tkFileDialog.askopenfilenames()
        self.file_list = list(files)
    
    def file_to_array(self, fn):
        with open(fn, 'rb') as open_file:
            self.data.append(np.array(open_file))
    
    def csv_to_array(self, fn):
        with open(fn, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')
            self.data.append(np.array(reader))

              
#-----Windows-----
#Left Window
class window_one(Window):
    def __init__(self, parent, *args, **kwargs):
        Window.__init__(self, parent, *args, **kwargs)
        #self.title("Window One")
        #Set window position (needs to happen last to account for widget sizes)
        #self.geometry("+%d+%d" % (0, 0))
        self.update()
        self.hpos = 0
        self.vpos = self.winfo_screenheight()/2 - self.winfo_height()/2
        self.geometry("+%d+%d" % ( self.hpos, self.vpos))

#Right Window
class window_two(Window):
    def __init__(self, parent, *args, **kwargs):
        Window.__init__(self, parent, *args, **kwargs)
        #set window position (needs to happen last to account for widget sizes)
        #self.geometry("+%d+%d" % (0, 0))
        self.update()
        self.hpos =  self.winfo_screenwidth() - self.winfo_width()
        self.vpos = self.winfo_screenheight()/2 - self.winfo_height()/2
        self.geometry("+%d+%d" % (self.hpos, self.vpos))

MainApp()
