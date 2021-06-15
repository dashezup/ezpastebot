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
import asyncio
import os
import re
import socket
from typing import Optional, Tuple

from pyrogram.types import Message

from utils.http import session

HTTP_MAX_ATTEMPT = 5
HTTP_TIMEOUT = 2
MAX_PASTE_SIZE = 1 * 1024 * 1024

pattern = re.compile(r'^text/|json$|yaml$|xml$|toml$')


async def ezpaste(m: Message) -> Tuple[Optional[str], Optional[str]]:
    if m.document and 0 < m.document.file_size <= MAX_PASTE_SIZE \
            and pattern.search(m.document.mime_type):
        filename = await m.download()
        with open(filename) as f:
            content = f.read()
        os.remove(filename)
    elif m.text:
        content = m.text
    else:
        return None, None
    paste_url = await _netcat('ezup.dev', 9999, content)
    preview_url = await get_preview_url(paste_url)
    return paste_url, preview_url


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


async def get_preview_url(url: str, try_once=False) -> Optional[str]:
    preview_url = f"{url}/preview.png"
    for _ in range(HTTP_MAX_ATTEMPT):
        try:
            async with session.head(preview_url, timeout=HTTP_TIMEOUT) as resp:
                status = resp.status
                content_length = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return None
        if try_once:
            return preview_url if status == 200 else None
        if status == 404 or (status == 200 and content_length == 0):
            await asyncio.sleep(0.4)
        else:
            return preview_url if status == 200 else None
    return None
