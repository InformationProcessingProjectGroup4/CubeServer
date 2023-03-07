import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key


def get_score(leaderboard):
    return leaderboard["score"]

def get_leaderboard(table, level, count):
    #begin the scan
    try:
        response = table.scan(
            FilterExpression='score[{}] > :val'.format(level),
            ExpressionAttributeValues={':val' : 0,})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}")
    else:
        data = response["Items"]
        #inlcude pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression='score[{}] > :val'.format(level),
                ExpressionAttributeValues={':val' : 0,},
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items']) #update if more results
        #initialise leaderboard array
        leaderboard = []
        for i in range(len(data)):
    	    leaderboard.append({"username": data[i]['username'], "score": data[i]['score'][level] })
        leaderboard.sort(key=lambda x : get_score(x), reverse=True)
        leaderboard = leaderboard[:count]
        return leaderboard

import json
from cubeserver.util import hash_password, check_password


# connect database
def db_connect(name):
    database = boto3.resource("dynamodb", region_name="eu-west-2")
    table = database.Table(name)
    return table

# -------------------------- progress branch --------------------------#

# PLEASE NOTE: IF WE ARE HANDLING JSONs AS-IS, WE MIGHT NOT BE ABLE TO USE A LIST [] FOR THE PROGRESS DATA


def get_user_progress(table, username):
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to get progress")
    else:
        if response["Item"]:
            user = response["Item"]
            if user["score"]:
                return user["progress"]
            else:
                return []
        else:
            return [] # default behaviour: empty list (no paused current state)


def get_user_score(table, username):
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to get score")
    else:
        if response["Item"]:
            user = response["Item"]
            if user["score"]:
                return user["score"]
            else:
                return [0, 0, 0, 0, 0]
        else:# default behaviour: 0 score
            return [0, 0, 0, 0, 0]


def get_user_level(table, username):
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to get level")
    else:
        if response["Item"]:
            user = response["Item"]
            if user["level"]:
                return user["level"]
            else:
                return [0,0,0,0,0]
        else:
            # default behaviour: no levels completed
            return [0, 0, 0, 0, 0]


def update_user_progress(table, username, progress_dict):
    progress= json.dumps(progress_dict)
    try:
        _ = table.update_item(Key={"username": username}, UpdateExpression="SET progress = :p", ExpressionAttributeValues={":p": progress})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to update progress")
    else:
        return


def update_user_score(table, username, score):
    try:
        _ = table.update_item(
            Key={"username": username}, UpdateExpression="SET score = :s", ExpressionAttributeValues={":s": score})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to update score")
    else:
        return
    

def update_user_level(table, username, level):
    try:
        _ = table.update_item(
            Key={"username": username}, UpdateExpression="SET levelV = :s", ExpressionAttributeValues={":s": level}) # level is a reserved keyword so we use levelV
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to update level")
    else:
        return

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
        if "Item" in response:
            return False
        
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
