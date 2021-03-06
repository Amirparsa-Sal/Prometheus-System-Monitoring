import socket
import psutil
import json
import time
import os

class Agent:
    '''This is a class for our agents to get system data and send it to our server.'''

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self) -> None:
        '''Connects agent's socket to server.'''
        self.socket.connect((self.host, self.port))
    
    def close(self) -> None:
        '''Closes agent's socket.'''
        self.socket.close()
    
    def send_message(self, message: str):
        '''Sends a string to the server.'''
        self.socket.send(message.encode('ascii'))

def get_sys_data():
    '''Gets system data using psutil and stores it to a dict.'''
    data = {
        "cpu_percent": psutil.cpu_percent(),
        "mem_available": psutil.virtual_memory().available,
    }
    return data

if __name__ == '__main__':
    # Create an agent
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    agent = Agent(host=host, port=8001)

    not_connected = True
    while not_connected:
        try:
            # Try to connect to the server
            agent.connect()
            not_connected = False
            print('Connected to the server!')
        except ConnectionRefusedError as e:
            print(e)

    try:
        while True:
            # Get system data
            data = get_sys_data()
            print(f'data: {data}')
            # Send data to server
            agent.send_message(json.dumps(data))
            # Wait 1s
            time.sleep(1)
    except ConnectionResetError:
        print("Connection to server closed unexpectedly!")
    except:
        print("An unknown error occured!")
        