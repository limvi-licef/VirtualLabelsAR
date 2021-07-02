import asyncio
import websockets
import nest_asyncio
import json
import time
import os
from threading import Thread

nest_asyncio.apply()

DEFAULT_IP_ADRESS = "0.0.0.0"
DEFAULT_PORT = 11000
DEFAULT_SAVED_LABELS_PATH = "labels.txt"


class Server:
    m_pathToLabelsFile = ""
    m_ip = ""
    m_port = 0

    def __init__(self, pathToLabels = DEFAULT_SAVED_LABELS_PATH, address=DEFAULT_IP_ADRESS, port=DEFAULT_PORT):
        self.m_pathToLabelsFile = pathToLabels
        self.m_ip = address
        self.m_port = port

    ##############################################################
    def read_labels(self):
        """Open the file at relative path (default:'labels.txt') from project source folder (HCI) and return the string"""

        file = open(self.m_pathToLabelsFile, "r")  # open file reading mode
        labels = file.read();

        print(labels)

        file.close()
        return labels

    def updatePathLabelsFile (self, path):
        print("[Server::updatePathLabelsFile] Called")
        self.m_pathToLabelsFile = path

    def start_loop(self, loop, server):
        loop.run_until_complete(server)
        loop.run_forever()

    def run(self):
        '''Run async server with address (default:'0.0.0.0') and port(default:11000). '''
        # This function is inspired by https://stackoverflow.com/questions/58123599/starting-websocket-server-in-different-thread-event-loop
        newloop = asyncio.new_event_loop()
        start_server = websockets.serve(self.connection, self.m_ip, self.m_port, loop=newloop)

        t = Thread(target=self.start_loop, args=(newloop, start_server))
        t.start()
        print("Server launched")
        time.sleep(2)

        # print("server started");
        # print("current data:")
        # self.read_labels()
        #
        # asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_forever()
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(start_server)
        # loop.close()

        print ("Hello.")

    def start (self):
        print ("Nothing for now")

    async def connection(self, client, path):
        '''Wait for a client to send request "GetLabels" to return data from "labels.txt"'''
        print("[Server:connection] Called - client connected")
        while True:
            try:
                message = await client.recv()
                print(f"[Server:connection] Received : {message}")

                if message == "GetLabels":
                    print("[Server:connection] Sending labels to Unity ... ")
                    labels = self.read_labels()
                    await client.send(labels)
                    print(f"[Server:connection] Labels sent")

            except websockets.exceptions.ConnectionClosedError:
                print("[Server:connection] client disconnected")
                break

#     @staticmethod
#     def runStatic(address=DEFAULT_IP_ADRESS, port=DEFAULT_PORT):
#         server = Server()
#         server.run_internal(address, port)
#
#
# if __name__ == "__main__":
#     Server.runStatic()

