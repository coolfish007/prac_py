# mecho.py

from socket import *

from examples.asyncio.echo_server import myasyncio
from examples.asyncio.echo_server.myasyncio import Loop

# myasyncio instead of asyncio interface
# loop = myasyncio.Loop()


async def echo_server(address, loop):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)

    while True:
        # yield唤醒后返回值,一直在循环里执行;
        # 符合echo_server的语义.会一直执行;每次accept一个连接后,会再次等待接收;
        client, addr = await loop.sock_accept(sock)
        print("Connection from: ", addr)
        loop.create_task(echo_handler(client, loop))


async def echo_handler(client, loop):
    # 从循环跳出意味着此func执行完了,返回后,造成此次调度器的send(None)抛出StopIteration异常.
    # 此handler执行完毕,符合handler的语义.
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            await loop.sock_sendall(client, b"Got: " + data)
    print("Connection closed")


# Listen on port 50000
# loop.create_task(echo_server(("", 50000)))
# loop.run_forever()
