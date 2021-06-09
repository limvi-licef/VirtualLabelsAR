import asyncio
import websockets
import nest_asyncio
import json
import time
nest_asyncio.apply()

address = "0.0.0.0"

def newID():
    return round(time.time() * 1000)

async def connection(client, path):
    print("client connected")
    while True:
        try :
            message = await client.recv()
            print(f"Received : {message}")
            
            if message == "GetLabels":
                print("Sending labels to Unity ... ")
                print(json.dumps(Label))
                await client.send(json.dumps(Label))
                print(f"Labels sent")
            
        except websockets.exceptions.ConnectionClosedError:
            print("client disconnected")
            break

start_server = websockets.serve(connection, address, 80)

print("server started");

# Create json labels coordinates for tests
Label = {}
Label["id"] = newID()
Label["position"] = [-1,0,1]
Label["orientation"] = [1,0,0]
Label["far"] = "Hello from Python"
Label["close"] = "Bonjour"


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
