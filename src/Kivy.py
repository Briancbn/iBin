#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 22:21:05 2017

@author: ZHI_WANG
"""

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App

from ValidId import return_points
from Ultrasonic_Sensor import is_full

ID=None
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
        enterButton = Button(text='OK')
        enterID.add_widget(self.enterIDText)
        enterID.add_widget(enterButton)
        #add Welcome and EnterID in the layout
        self.layout.add_widget(Welcome)
        self.layout.add_widget(enterID)
        #bind the enterButton to change screen function
        self.settings.bind(on_press=self.change_to_2)
        self.add_widget(self.layout)
    
    def change_to_UserInterface(self, value):
        self.id=self.enterIDText.text
        #update ID
        self.manager.transition.direction = 'right'
        # modify the current screen to a different "name"
    	self.manager.current= 'Screen2'

#    def quit_app(self, value):
#        App.get_running_app().stop()


class UserInterface(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        #information of the person
        self.information = GridLayout(cols=2)
        ID = Label(text='ID')
        IDText = Label(text=self.id)
        currentPoint = Label(text='Current Points')
        currentPointText = Label(text=return_points(IDText,"points"),
                                  color=(1,0,0,1))
        self.information.add_widget(ID)
        self.information.add_widget(IDText)
        self.information.add_widget(currentPoint)
        self.information.add_widget(currentPointText)
        # instruction
        instruction = Label(text="Throw the trash in the bin. Press Quit to exit")
        #quit button
        Quit = Button(text="Quit")
        #Add
        self.layout.add_widget(self.information)
        self.layout.add_widget(instruction)
        self.layout.add_widget(Quit)
        #bind exit
        self.BackToMenu.bind(on_press=self.change_to_Welcome)
        self.add_widget(self.layout)
        

    def change_to_Welcome(self,value):
        self.manager.transition.direction = 'left'
        # modify the current screen to a different "name"
        self.manager.current= 'w'


class FullBin(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=Label(text="The bin is full!",
                          color=(1,0,0,1),
                          size=40)
        # Add your code below to add the label and the button
        self.add_widget(self.layout)
        

class SwitchScreenApp(App):
	def build(self):
            self.id = ''
            sm=ScreenManager()
            w=Welcome(name='welcome')
            ui=UserInterface(name='user interface')
            fb=FullBin(name='full bin')
            sm.add_widget(w)
            sm.add_widget(ui)
            sm.add_widget(fb)
            sm.current='welcome'
            while is_full():
                sm.current='full bin'
            return sm

if __name__=='__main__':
	SwitchScreenApp().run()
