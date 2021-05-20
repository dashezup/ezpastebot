"""
ezpastebot, Telegram pastebin bot for https://ezup.dev/p/
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
