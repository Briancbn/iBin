#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 22:21:05 2017

@author: ZHI_WANG
"""

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from time import sleep, time

from ValidId import return_points, add_points
from Ultrasonic_Sensor import is_full
from loadCell import getGram

import sys
sys.path.append('../MFRC522-python')
from Read import ReturnID


class IDstorage(object):
    def __init__(self):
        self.ID=''
        self.name = ''
        self.points = 0
    
    def clear(self):
        self.ID=''
        self.name = ''
        self.points = 0
#create an ID object

identity=IDstorage()
tolerance = 10
timetol = 10
startpoints = 0
starttime = time()

class Welcome(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        #add Welcome label
        self.Welcome = Label(text='[size=50]Welcome![/size]\n[size=30]Please enter you ID below[/size]',
                             color = (1, 0.647059, 0,1), #orange
                             markup = True, 
                             size_hint=(.7, 1),
                             background_color = [1,1,1,1])
        #add the enter boxlayout
        enterID = BoxLayout(orientation='horizontal',
                            #padding = [5,3,5,3],
                            size_hint = (.3, 1))
        self.enterIDText = TextInput(multiline=False,
                                     padding = (3,3),
                                     size = 30)
        self.enterButton = Button(text='OK',
                                  padding = (2,5),
                                  background_color = [0.564706, 0.933333, 0.564706,1])
        enterID.add_widget(self.enterIDText)
        enterID.add_widget(self.enterButton)
        #add Welcome and EnterID in the layout
        self.layout.add_widget(self.Welcome)
        self.layout.add_widget(enterID)
        #bind the enterButton to change screen function
        self.enterButton.bind(on_press=self.change_to_UserInterface)
        Clock.schedule_interval(self.readcard, 1)
        Clock.schedule_interval(self.isfull, 1)
        self.add_widget(self.layout)
    
    def change_to_UserInterface(self, value):
        #update ID
        ID = self.enterIDText.text
        info = return_points(ID)
        # modify the current screen to a different "name"
        if self.manager.current == 'welcome' and info != False:
            identity.ID = info['ID']
            identity.name = info['name']
            identity.points = info['points']
            global startpoints, starttime
            startpoints = getGram()
            starttime = time()
            self.enterIDText.text = ''
            self.manager.transition = SlideTransition()
            self.manager.transition.direction = 'right'
            self.manager.current= 'user_interface'
        elif info == False:
            self.Welcome.text = "[size=50]Welcome![/size]\n[size=30]Please enter you ID below[/size]\n[color=FF6347]Please enter valid ID or Name" 
            self.enterIDText.text = ''
            
        
    def readcard(self, value):
      if self.manager.current == 'welcome':

        IDfromCard = ReturnID()
        if IDfromCard != False:
            info = return_points(IDfromCard)
            if info != False:
                identity.ID = info['ID']
                identity.name = info['name']
                identity.points = info['points']
                global startpoints, starttime
                self.enterIDText.text=''
                startpoints = getGram()
                starttime = time()
                self.manager.transition = SlideTransition()
                self.manager.transition.direction = 'right'
                # modify the current screen to a different "name"
                self.manager.current= 'user_interface'
        
    def isfull(self, value):
        if self.manager.current == 'welcome' or self.manager.current == 'full_bin':
            full = is_full()
            if full and self.manager.current == 'welcome':
                self.manager.transition = SlideTransition()
                self.manager.transition.direction = 'left'
                self.manager.current = "full_bin"
                sleep(1)
            elif not full and self.manager.current == 'full_bin':
                self.manager.transition = SlideTransition()
                self.manager.transition.direction = 'right'
                self.manager.current = "welcome"
                sleep(1)
#    def quit_app(self, value):
#        App.get_running_app().stop()


class UserInterface(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        #information of the person
        self.information = GridLayout(cols=2,
                                      background_color = [1,0.894118,0.882353,0.7])
        ID = Label(text='[b]ID[/b]',
                   color = (0,0,0,1),
                   markup = True)
        self.IDText = Label(text=identity.name,
                            color = (0,0,0,1))#black
        currentPoint = Label(text='[b]Current Points[/b]',
                             color = (0,0,0,1),#black
                             markup = True)
        self.currentPointText = Label(text=str(identity.points),#return_points(IDText,"points"),
                                 color=(0.564706, 0.933333, 0.564706,1))#green
        self.information.add_widget(ID)
        self.information.add_widget(self.IDText)
        self.information.add_widget(currentPoint)
        self.information.add_widget(self.currentPointText)
        # instruction
        self.instruction = Label(text="Throw the trash in the bin. Press [color=FF6347][b]Quit[/b][/color] to exit",
                                 markup = True)
        #quit button
        self.Quit = BoxLayout(cols=1,
                              padding = [20,3,0,0])
        self.QuitButton = Button(text="[size=30]Quit[/size]",
                                 color = (1, 0.388235, 0.278431,1),
                                 markup = True)
        self.Quit.add_widget(self.QuitButton)
        #Add
        self.layout.add_widget(self.information)
        self.layout.add_widget(self.instruction)
        self.layout.add_widget(self.Quit)
        #bind exit
        self.QuitButton.bind(on_press=self.change_to_Welcome)
        self.add_widget(self.layout)
        Clock.schedule_interval(self.update_name_points, 1)

        
    def update_name_points(self, value):
        if self.manager.current == "user_interface":
            self.IDText.text=identity.name
            self.currentPointText.text=str(identity.points)
            global startpoints, starttime, tolerance
            newpoints = getGram()
            if startpoints > 100:
                tolerance = 0.1 * startpoints
            if newpoints > startpoints + tolerance or newpoints < startpoints - tolerance:
                identity.points += newpoints - startpoints
                startpoints = newpoints
                starttime = time()
            newtime = time()
            timelapse = newtime - starttime
            if timetol > timelapse >= timetol - 5:
                self.instruction.text = "Quit in %is" % int(timetol + 1 - timelapse)
            elif timelapse < 5:
                self.instruction.text = "Throw the trash in the bin. Press [color=FF6347][b]Quit[/b][/color] to exit"
            else:
                self.change_to_Welcome(0)
                
            

    def change_to_Welcome(self,value):
        add_points(identity.ID, identity.points)
        print identity.points
        identity.clear()
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'left'
        # modify the current screen to a different "name"
        self.manager.current= 'welcome'
        sleep(1)


class FullBin(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=Label(text="The bin is full!",
                          color=(1,0,0,1))
        # Add your code below to add the label and the button
        self.add_widget(self.layout)
        

class SwitchScreenApp(App):
	def build(self):
            sm=ScreenManager()
            w=Welcome(name='welcome')
            ui=UserInterface(name='user_interface')
            fb=FullBin(name='full_bin')
            sm.add_widget(w)
            sm.add_widget(ui)
            sm.add_widget(fb)
            sm.current='welcome'
            #update the id and the currentPoints
#            while is_full():
#                sm.current='full_bin'
            return sm

if __name__=='__main__':
	SwitchScreenApp().run()
