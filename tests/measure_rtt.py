import time
import json
import requests

# constatns
URL_HOST = "ec2-35-177-122-51.eu-west-2.compute.amazonaws.com"
URL_PORT = "5000"
TEST_API = ["/api", "/api/progress"]
TEST_DATA = [{}, { "username": "samuelpswang" }]
COUNT = 20

# measure rtt
start = time.time()
for i in range(len(TEST_API)):
    start = time.time()
    for j in range(COUNT):
        response = requests.put("http://"+URL_HOST+":"+URL_PORT+TEST_API[i], \
            json=TEST_DATA[i],
            headers={'Content-Type': 'application/json'})
        if str(response.status_code) != str(200): 
            print(f"{response.status_code}: {json.loads(response.content.decode('utf-8'))}")
    end = time.time()
    rtt = ((end-start)/COUNT)*1000
    print("---")
    print(f"api: {TEST_API[i]}")
    print(f"test data: {TEST_DATA[i]}")
    print(f"request count: {COUNT}")
    print(f"rtt: {rtt} ms")
    print("---")
