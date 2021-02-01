from examples.asyncio.echo_server.myasyncio import Loop
from examples.asyncio.echo_server.mecho import echo_server


def test_mecho():
    loop = Loop()
    loop.create_task(echo_server(("", 49999), loop))
    loop.run_forever()
