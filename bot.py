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

from pyrogram import Client, idle

from utils.http import session

plugins = dict(
    root="plugins",
    include=[
        "commands",
        "inline",
        "private_non_reply"
    ]
)


async def main():
    app = Client("ezpastebot", plugins=plugins)
    await app.start()
    print('>>> BOT STARTED')
    await idle()
    await session.close()
    print('\n>>> BOT STOPPED')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
