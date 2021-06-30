import asyncio
import websockets
import nest_asyncio
import json
import time
import os

nest_asyncio.apply()

DEFAULT_IP_ADRESS = "0.0.0.0"
DEFAULT_PORT = 11000
DEFAULT_SAVED_LABELS_PATH = "labels.txt"


class Server:

    ##############################################################
    def read_labels(self, path=DEFAULT_SAVED_LABELS_PATH):
        """Open the file labels.txt in project source folder (HCI) and return the string"""

        print(os.path.dirname(__file__))
        file = open(path, "r")  # open file on override reading mode
        labels = file.read();
        print(labels)
        file.close()
        return labels

    def run_internal(self, address=DEFAULT_IP_ADRESS, port=DEFAULT_PORT):
        start_server = websockets.serve(self.connection, address, port)
        self.read_labels()

        print("server started");

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def connection(self, client, path):
        print("client connected")
        while True:
            try:
                message = await client.recv()
                print(f"Received : {message}")

                if message == "GetLabels":
                    print("Sending labels to Unity ... ")
                    labels = self.read_labels()
                    await client.send(labels)
                    print(f"Labels sent")

            except websockets.exceptions.ConnectionClosedError:
                print("client disconnected")
                break

    @staticmethod
    def run(address=DEFAULT_IP_ADRESS, port=DEFAULT_PORT):
        server = Server()
        server.run_internal(address, port)


if __name__ == "__main__":
    Server.run()

