import asyncio
import logging
import socket
from concurrent.futures import TimeoutError


async def connect(host='minechat.dvmn.org', port=5000, attempts=10, timeout=2):
    while attempts:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            return reader, writer
        except socket.gaierror:
            print(f'Cannot connect to {host}:{port}. Next retry in {timeout} seconds. {attempts} attempts lost')
            attempts -= 1
            timeout += 2
            await asyncio.sleep(timeout)
    print(f'Abort connecting to {host}:{port}')
    raise asyncio.CancelledError


async def read_chat(host='minechat.dvmn.org', port=5000):
    reader, writer = await connect()
    print(f'Start listening to {host}:{port}')

    try:
        while not reader.at_eof():
            try:
                line = await asyncio.wait_for(reader.readline(), 11)
                line = line.decode().rstrip()
                print(f'Received: {line}')
            except TimeoutError:
                print('No connection. Try to reconnect...')
                writer.close()
                reader, writer = await connect()

    finally:
        print('Close the connection...')
        writer.close()


if __name__ == '__main__':
    # logging.getLogger("asyncio").setLevel(logging.DEBUG)
    try:
        asyncio.run(read_chat())
    except KeyboardInterrupt:
        print('Interrupted by user.')
    except asyncio.CancelledError:
        print('Bye!')
