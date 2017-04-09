from kivy.app import App 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.togglebutton import ToggleButton
from firebase import firebase

url = "https://kivy-aa39a.firebaseio.com/" # URL to Firebase database
token = "CEg81kbsyacNiXHTK1919veba3Ow4t258E5wekMm" # unique token used for authentication

#url = "https://hello-world-88fde.firebaseio.com/" # URL to Firebase database
#token = "GMaV7uDBSzolO6onUBNA2VKm0OaEMEib4yfGUWKL" # unique token used for authentication


firebase=firebase.FirebaseApplication(url,token)

class GuiKivy(App):
    
    def build(self):
        layout=GridLayout(cols=2)
        # add your widget to the layout
        RedLabel=Label(text='Red')
        YellowLabel=Label(text='Yellow')
        self.RedToggle=ToggleButton(text='off')
        self.YellowToggle=ToggleButton(text='off')
        
        layout.add_widget(RedLabel)
        layout.add_widget(self.RedToggle)
        layout.add_widget(YellowLabel)
        layout.add_widget(self.YellowToggle)
        
        self.RedToggle.bind(on_press=self.OnRed)
        self.YellowToggle.bind(on_press=self.OnYellow)
        
        return layout
    
#    def updateStatus(self, instance):
#        red = firebase.get('/red')
#        yellow = firebase.get('/yellow')


    def OnRed(self,instance):
        if self.RedToggle.text=='on':
            self.RedToggle.text='off'
        else:
            self.RedToggle.text='on'
        
        firebase.put('/' , 'red', self.RedToggle.text)
    
    def OnYellow(self,instance):
        if self.YellowToggle.text=='on':
            self.YellowToggle.text='off'
        else:
            self.YellowToggle.text='on'
        firebase.put('/' , 'yellow', self.YellowToggle.text)

GuiKivy().run()