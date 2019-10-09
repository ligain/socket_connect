import asyncio
import logging


async def read_chat(host='minechat.dvmn.org', port=5001):
    reader, writer = await asyncio.open_connection(host, port)

    print(f'Start listening on: {host}:{port}')

    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            line = line.decode().rstrip()
            print(f'Received: {line}')
    finally:
        print('Close the connection...')
        writer.close()

try:
    asyncio.run(read_chat())
except KeyboardInterrupt:
    print('Interrupted by user.')
