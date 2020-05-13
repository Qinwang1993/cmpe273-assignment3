import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from lru_cache import lru_cache

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        hash_codes.add(str(response.decode()))


    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)


def put(udp_clients, obj):
    client_ring = NodeRing(udp_clients)
    data_bytes, key = serialize_PUT(obj)
    response = client_ring.get_node(key).send(data_bytes)
    print(response)


def delete(udp_clients, hc):
    client_ring = NodeRing(udp_clients)
    data_bytes, key = serialize_DELETE(hc)
    response = client_ring.get_node(key).send(data_bytes)
    print (response)


@lru_cache(5)
def get(udp_clients, hc):
    client_ring = NodeRing(udp_clients)
    data_bytes, key = serialize_GET(hc)
    response = client_ring.get_node(key).send(data_bytes)
    print (response)    


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
    
    while True:
        line = sys.stdin.readline()
        operation = line.split(",")[0].strip()
        if operation == "delete" or operation == "DELETE":
            hc = line.split(",")[1].strip()
            delete(clients, hc)
        elif operation == "get" or operation == "GET":
            hc = line.split(",")[1].strip()
            get(clients, hc)
        elif operation == "exit" and operation == "EXIT":
            break
        else:
            print ("Re-input operation!")
        
    
