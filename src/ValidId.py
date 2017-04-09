### Communications with the firebase ###
from firebase import firebase

url = "https://ddigitalworld-20118.firebaseio.com/" #unique to project
token = "Czk1K09ZNHtLLOfRLdIe6htAzeWwrqYwJTnbrOqN" #unique token used for authentication

firebase = firebase.FirebaseApplication(url, token)

database_id = [{"ID": "iidd1", "name": "Marcus", "points": "420"}, {"ID": "iidd2", "name": "Suwen", "points": "477"}]
firebase.put("/", "DW" , database_id)
deek = firebase.get("/DW")


def return_points(ID, points, database_id):
    for entry in deek:
        if ID == entry["ID"]:
           return  entry[points]


    # need set to retrieve value from firebase and store as local variable
    # database ID should be a dictionary





    
