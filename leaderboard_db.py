import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

#def db_connect(name):
 #   database = boto3.resource("dynamodb", region_name="us-east-2")
  #  table = database.Table(name)
   # return table

def get_score(leaderboard):
    return leaderboard["score"]

def get_leaderboard(level,count, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    table = dynamodb.Table('CubeServerData')

    response = table.scan(
    FilterExpression='score[{}] > :val'.format(level),
    ExpressionAttributeValues={':val' : 0,}
    )
    data = response["Items"]
    #except Exception as e:
     #   raise Exception(f"DatabaseException: {str(e)}")
   # else:
    leaderboard = []
    for i in range(len(data)):
    	leaderboard.append({"username": data[i]['username'], "score": data[i]['score'][level] })
    leaderboard.sort(key=lambda x : get_score(x), reverse=True)
    leaderboard = leaderboard[:count]
    return leaderboard

if __name__ == '__main__':
    entries = get_leaderboard(1, 2)
    print("retrieved leaderboard succesfully")
    print(entries)
