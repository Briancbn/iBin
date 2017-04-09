### Communications with the firebase ###
from firebase import firebase

url = "https://ddigitalworld-20118.firebaseio.com/" #unique to project
token = "Czk1K09ZNHtLLOfRLdIe6htAzeWwrqYwJTnbrOqN" #unique token used for authentication

firebase = firebase.FirebaseApplication(url, token)

database_id = [{"ID": "64,237,132,124", "name": "Marcus", "points": 0}, {"ID": "80,106,203,128", "name": "Suwen", "points": 0}]
firebase.put("/", "DW" , database_id)
deek = firebase.get("/DW")


def return_points(ID, points):
    for entry in deek:
        if ID == entry["ID"]:
           return  entry[points]
  
def update_points(ID, newpoints):
    for entry in deek:
        if ID == entry["ID"]:
            entry["points"] += newpoints
            firebase.put("/", "DW", deek)
            return entry["points"]
