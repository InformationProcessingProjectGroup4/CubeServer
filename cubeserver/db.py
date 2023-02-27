import boto3
from datetime import datetime
from cubeserver.util import hash_password, check_password


# connect database
def db_connect(name):
    database = boto3.resource("dynamodb", region_name="eu-west-2")
    table = database.Table(name)
    return table


# user functions
def add_user(table, username, password):
    # build record
    hash = hash_password(password)
    record = {
        "username": username,
        "password": hash,
        "updated": str(datetime.now()),
        "score": [0, 0, 0, 0, 0],
        "level": [0, 0, 0, 0, 0],
        "progress": []
    }
    
    # check if usernmae is duplicate
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}")
    else:
        if not response["Item"]:
            raise Exception(f"DuplicateUsernameException: username ({username}) is already in database")
        
    # add record
    try: 
        table.put_item(Item=record)
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}")
    else:
        return True


def auth_user(table, username, password):
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}")
    else:
        if response["Item"]:
            user = response["Item"]
            return check_password(password, user["password"])
        else:
            return False # username or password incorrect
