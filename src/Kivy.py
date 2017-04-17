#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 22:21:05 2017

@author: ZHI_WANG
"""

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock

from ValidId import return_points
from Ultrasonic_Sensor import is_full

import sys
sys.path.append('../MFRC522-python')
from Read import ReturnID


class IDstorage(object):
    def __init__(self,ID='0'):
        self.ID=ID
#create an ID object
id1=IDstorage()

class Welcome(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        #add Welcome label
        Welcome = Label(text='[size=30]Welcome![/size]\n[size=20]Please enter you ID below[/size]',
                        color = (0,0,1,1))
        #add the enter boxlayout
        enterID = BoxLayout(orientation='horizontal')
        self.enterIDText = TextInput(multiline=False)
        self.enterButton = Button(text='OK')
        enterID.add_widget(self.enterIDText)
        enterID.add_widget(self.enterButton)
        #add Welcome and EnterID in the layout
        self.layout.add_widget(Welcome)
        self.layout.add_widget(enterID)
        #bind the enterButton to change screen function
        self.enterButton.bind(on_press=self.change_to_UserInterface)
        self.check_card = Clock.schedule_interval(self.readcard, 0.1)
        self.check_full = Clock.schedule_interval(self.isfull, 0.1)
        self.add_widget(self.layout)
    
    def change_to_UserInterface(self, value):
        id1.ID=self.enterIDText.text
        self.enterIDText.text=''
        #update ID
        # modify the current screen to a different "name"
        if self.manager.current == 'welcome':
            self.manager.transition = SlideTransition
            self.manager.transition.direction = 'right'
            self.manager.current= 'user_interface'
        
    def readcard(self, value):
      if self.manager.current == 'welcome':

        IDfromCard = ReturnID()
        if IDfromCard != False:
            id1.ID=IDfromCard
            self.enterIDText.text=''
            #update ID
            self.manager.transition = SlideTransition
            self.manager.transition.direction = 'right'
            # modify the current screen to a different "name"
            self.manager.current= 'user_interface'

        
    def isfull(self, value):
        if self.manager.current == 'welcome' or self.manager.current == 'full_bin':
            if is_full():
                self.manager.transition = NoTransition()
                self.manager.current = "full_bin"
            else:
                self.manager.transition = NoTransition()
                self.manager.current = "welcome"
#    def quit_app(self, value):
#        App.get_running_app().stop()


class UserInterface(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        #information of the person
        self.information = GridLayout(cols=2)
        ID = Label(text='ID')
        self.IDText = Label(text='0')
        currentPoint = Label(text='Current Points')
        self.currentPointText = Label(text='111',#return_points(IDText,"points"),
                                 color=(1,0,0,1))
        self.information.add_widget(ID)
        self.information.add_widget(self.IDText)
        self.information.add_widget(currentPoint)
        self.information.add_widget(self.currentPointText)
        # instruction
        instruction = Label(text="Throw the trash in the bin. Press Quit to exit")
        #quit button
        self.Quit = Button(text="Quit")
        #Add
        self.layout.add_widget(self.information)
        self.layout.add_widget(instruction)
        self.layout.add_widget(self.Quit)

        #bind exit
        self.Quit.bind(on_press=self.change_to_Welcome)
        self.add_widget(self.layout)
        
    def update_id_and_points(self,value):
        self.IDText.text=id1.ID
        #self.currentPointText=return_points(IDText,"points")

    def change_to_Welcome(self,value):
        id1.ID='0'
        self.manager.transition = NoTransition
        # modify the current screen to a different "name"
        self.manager.current= 'welcome'


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
