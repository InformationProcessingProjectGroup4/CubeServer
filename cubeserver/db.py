import boto3
from datetime import datetime

import json


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
            Key={"username": username}, UpdateExpression="SET level = :l", ExpressionAttributeValues={":l": level})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to update level")
    else:
        return
