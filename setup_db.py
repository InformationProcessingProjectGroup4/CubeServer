import boto3

def create_user_table(database=None):
    if not database:
        database = boto3.resource("dynamodb", region_name="eu-west-2")
    
    table = database.create_table( # type: ignore
        TableName="CubeServerData",
        KeySchema=[{ "AttributeName": "username", "KeyType": "HASH"}],
        AttributeDefinitions=[{ "AttributeName": "username", "AttributeType": "S"}],
        ProvisionedThroughput={ "ReadCapacityUnits": 10, 
                                "WriteCapacityUnits": 10 }
    )
    
    return table

if __name__ == "__main__":
    print(f"[cubeserver] Creating \"CubeServerData\" table...")
    table = create_user_table()
    print(f"[cubeserver] Table \"CubeServerData\" status: {table.table_status}.")
    