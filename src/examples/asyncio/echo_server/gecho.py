#gecho.py

from gevent.server import StreamServer

def echo(socket, address):
    print("Connection from: ", address)
    while True:
        data = socket.recv(100000)
        if not data:
            break
        socket.sendall(b'Got: '+data)
    socket.close()
    print("Connection closed")

if __name__ == "__main__":
    server = StreamServer(("localhost", 50000), echo)
    server.serve_forever()
