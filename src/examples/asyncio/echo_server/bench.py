#bench.py

from socket import *
import time

def benchmark(addr, messages):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(addr)
    start = time.time()
    for n in range(messages):
        sock.send(b'x')
        resp = sock.recv(10000)
    end = time.time()
    print(messages/(end-start), "messages/sec")

benchmark(("localhost", 50000), 100000)
