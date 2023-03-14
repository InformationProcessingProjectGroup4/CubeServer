import boto3
import json
from datetime import datetime

from cubeserver.util import hash_password, check_password


# ----------------------------- Basic Operations ----------------------------- #

def db_connect(name):
    database = boto3.resource("dynamodb", region_name="eu-west-2")
    table = database.Table(name)
    return table

# --------------------------------- /api/user -------------------------------- #

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
        if "Item" in response:
            user = response["Item"]
            return check_password(password, user["password"])
        else:
            return False # username or password incorrect


# ------------------------------- /api/progress ------------------------------ #

# PROGRESS FEATURE IS NOT YET CONFIRMED

def get_user_data(table, username):
    try:
        response = table.get_item(Key={"username": username})
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to get data")
    else:
        if "Item" in response:
            return(response["Item"])
        else:  # default behaviour: 0 score
            raise Exception(f"DatabaseException: {str(e)}, failed to get data")


# def get_user_progress(table, username):
#     try:
#         response = table.get_item(Key={"username": username})
#     except Exception as e:
#         raise Exception(f"DatabaseException: {str(e)}, failed to get progress")
#     else:
#         if "Item" in response:
#             user = response["Item"]
#             if user["score"]:
#                 return user["progress"]
#             else:
#                 return []
#         else:
#             return [] # default behaviour: empty list (no paused current state)


# def get_user_score(table, username):
#     try:
#         response = table.get_item(Key={"username": username})
#     except Exception as e:
#         raise Exception(f"DatabaseException: {str(e)}, failed to get score")
#     else:
#         if "Item" in response:
#             user = response["Item"]
#             if user["score"]:
#                 return user["score"]
#             else:
#                 return [0, 0, 0, 0, 0]
#         else: # default behaviour: 0 score
#             return [0, 0, 0, 0, 0]

# def get_user_level(table, username):
#     try:
#         response = table.get_item(Key={"username": username})
#     except Exception as e:
#         raise Exception(f"DatabaseException: {str(e)}, failed to get level")
#     else:
#         if "Item" in response:
#             user = response["Item"]
#             if user["level"]:
#                 return user["level"]
#             else:
#                 return [0,0,0,0,0]
#         else:
#             # default behaviour: no levels completed
#             return [0, 0, 0, 0, 0]

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
            Key={"username": username}, UpdateExpression="SET #lv = :l", ExpressionAttributeValues={":l": level}, ExpressionAttributeNames={"#lv": "level"})  # level is a reserved keyword so we use the ExpressionAttributeNames placeholder function
    except Exception as e:
        raise Exception(f"DatabaseException: {str(e)}, failed to update level")
    else:
        return


# ----------------------------- /api/leaderboard ----------------------------- #

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
        
        # leaderboard: [{ "username": str, "score": int }]
        result = { "username": [], "score": [], "level": level }
        for entry in leaderboard:
            result["username"].append(entry["username"])
            result["score"].append(entry["score"])
        
        return result
