### Communications with the firebase ###
from firebase import firebase

url = "https://ddigitalworld-20118.firebaseio.com/" #unique to project
token = "Czk1K09ZNHtLLOfRLdIe6htAzeWwrqYwJTnbrOqN" #unique token used for authentication

firebase = firebase.FirebaseApplication(url, token)
