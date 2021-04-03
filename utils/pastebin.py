import os
import socket
from pyrogram.types import Message


async def ezpaste(m: Message):
    if m.document and 0 < m.document.file_size <= 1048576 \
            and m.document.mime_type.split('/')[0] == "text":
        filename = await m.download()
        with open(filename) as f:
            content = f.read()
        os.remove(filename)
    elif m.text:
        content = m.text
    else:
        return None
    url = await _netcat('ezup.dev', 9999, content)
    return url


async def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode('utf-8').strip('\n\x00')
        if not data:
            break
        return data
    s.close()
