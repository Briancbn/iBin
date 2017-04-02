def check_id(identity)
# identity should be either from CardRead or Userinput
    firebase.get("/") database_id =
    # need set to retrieve value from firebase and store as local variable
    # database ID should be a dictionary
    
    if identity in database_id.keys()
        return True

    else:
        return False


def current_points(identity):
    # returns current points
    database_id =
    # need set to retrieve value from firebase and store as local variable
    return database_id[identity]
