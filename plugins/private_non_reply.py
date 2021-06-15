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
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from utils.pastebin import ezpaste

reply_filter = filters.create(lambda _, __, m: m.reply_to_message)


@Client.on_message(
    filters.private
    & (filters.document | filters.text)
    & ~reply_filter
    & ~filters.regex(r"^\/")
)
async def ask_to_paste(_, m: Message):
    await m.reply_text(
        "Do you want to upload this paste?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes",
                        callback_data="yes_upload_paste"
                    ),
                    InlineKeyboardButton(
                        "Ignore",
                        callback_data="ignore_paste"
                    )
                ]
            ]
        ),
        quote=True
    )


@Client.on_callback_query(filters.regex(r"^yes_upload_paste$"))
async def upload_paste(_, cq: CallbackQuery):
    url, _ = await ezpaste(cq.message.reply_to_message)
    if not url:
        return
    share_url = (
        f"https://t.me/share/url?url={url}"
        "&text=%E2%80%94%20__Pasted%20with__"
        "%20%F0%9F%A4%96%20%40ezpastebot"
    )
    await cq.message.edit_text(
        url,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Share",
                        url=share_url
                    ),
                    InlineKeyboardButton(
                        "Inline",
                        switch_inline_query=url
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex(r"^ignore_paste$"))
async def ignore(_, cq: CallbackQuery):
    await cq.message.delete()
