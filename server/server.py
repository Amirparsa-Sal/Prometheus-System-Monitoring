from audioop import add
import socket
import json
from _thread import *
import threading
from prometheus_client import start_http_server, Gauge
import time

# Create gauges
cpu_gauge = Gauge('cpu_percent', 'CPU Utilization Percent', ['agent'])
mem_gauge = Gauge('mem_available', 'Available Memory', ['agent'])

def send_data(message: str, agent_id: int):
    '''This is a function to send data to Prometheus server.'''
    # Convert data message to json
    data = json.loads(message)
    agent_string = f'agent {agent_id}'
    # Update graphs
    cpu_gauge.labels(agent=agent_string).set(data['cpu_percent'])
    mem_gauge.labels(agent=agent_string).set(data['mem_available'])


class Server:
    '''This is a class for our server to receive data from agents and send it to Prometheus server.'''

    def __init__(self, port) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", port))
        self.print_lock = threading.Lock()
        self.agents_num = 0
        self.agents = dict()
        self.start_time = 0

    def listen(self, max_connections: int = 5):
        self.socket.listen(max_connections)
        self.start_time = time.time()
        print('Server is up!')
        
        while True:
            # establish connection with agent
            socket, addr = self.socket.accept()

            # Generate an ID for the agent
            self.agents_num += 1
            self.agents[socket] = self.agents_num

            # Lock stdout to avoid race conditions and print connection message
            self.print_lock.acquire()
            print(f'Connected to client {self.agents_num} with address={addr[0]} and port={addr[1]}, time={time.time() - self.start_time}')
            self.print_lock.release()

            # Start a new thread to handle agent
            start_new_thread(self.handle_agent, (socket,))

    def handle_agent(self, socket: socket.socket):
        # Retreive agent id from agents dict
        agent_id = self.agents[socket]
        try:
            while True:
                # Receive data from client
                data = socket.recv(1024)
                # Send data to Prometheus;;
                send_data(data, agent_id)
        except ConnectionResetError:
            # delete agent from agents dict
            del self.agents[socket]
            self.print_lock.acquire()
            print(f"Client {agent_id}'s connection forcibly closed! total connections: {len(self.agents)}")
            self.print_lock.release()
    
if __name__ == '__main__':
    # Start Prometheus server
    start_http_server(8080)
    # Start our server
    server = Server(port=8001)
    server.listen()