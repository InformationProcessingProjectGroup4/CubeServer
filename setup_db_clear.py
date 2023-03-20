import boto3

def delete_user_table(database=None):
    if not database:
        database = boto3.resource("dynamodb", region_name="eu-west-2")
    
    try:
        table = database.Table("CubeServerData")  # type: ignore
        table.delete()
    except Exception as e:
        print(e)
        return False
    finally:
        return True

if __name__ == "__main__":
    print(f"[cubeserver] Deleting \"CubeServerData\" table...")
    status = delete_user_table()
    if status:
        print(f"[cubeserver] Table \"CubeServerData\" deleted.")
    else:
        print(f"[cubeserver] Table \"CubeServerData\" deletion failed.")
