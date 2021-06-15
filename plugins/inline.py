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
from typing import List, Union

from pyrogram import Client, filters
from pyrogram.types import (InlineQuery, Message,
                            InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            InlineQueryResultPhoto,
                            ForceReply)

from utils.pastebin import ezpaste, get_preview_url

ASK_TO_SEND_PASTE = "Send paste"


async def answer_with_paste_filter(_, __, m: Message):
    reply = m.reply_to_message
    if reply and reply.from_user.is_self and reply.text == ASK_TO_SEND_PASTE:
        return True
    return False


answer_with_paste = filters.create(answer_with_paste_filter)


@Client.on_inline_query()
async def answer(_, iq: InlineQuery):
    query = iq.query
    if query.startswith('https://ezup.dev/p/') and len(query) == 25:
        iq_results = await make_iq_results(query)
        await iq.answer(
            results=iq_results,
            cache_time=1
        )
        return
    await iq.answer(
        results=[],
        cache_time=1,
        switch_pm_text="Send paste in PM",
        switch_pm_parameter="from_inline"
    )


async def make_iq_results(url: str) -> List[Union[InlineQueryResultArticle,
                                                  InlineQueryResultPhoto]]:
    preview_url = await get_preview_url(url)
    url_raw = f"{url}/index.txt"
    paste_id = url[19:]
    paste_info = f"ezpaste: [{paste_id}]({url}) | [raw]({url_raw})"
    share_url = (
        f"https://t.me/share/url?url={url}"
        "&text=%E2%80%94%20__Pasted%20with__"
        "%20%F0%9F%A4%96%20%40ezpastebot"
    )
    results = [
        InlineQueryResultArticle(
            title="Send URL of this paste",
            input_message_content=InputTextMessageContent(
                paste_info
            ),
            url=url,
            description="A paste on ezup.dev/p",
            thumb_url=preview_url,
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
    ]
    if preview_url:
        results.append(
            InlineQueryResultPhoto(
                photo_url=preview_url,
                thumb_url=preview_url,
                title="Send preview image of this paste",
                description="up to the first 79 lines of the paste",
                caption=paste_info,
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
        )
    return results


@Client.on_message(filters.private & filters.regex(r'^\/start from_inline$'))
async def receive_private_message(_, m: Message):
    await m.reply_text(ASK_TO_SEND_PASTE, reply_markup=ForceReply())


@Client.on_message(filters.private & answer_with_paste)
async def reply_with_text(_, m: Message):
    url, _ = await ezpaste(m)
    if not url:
        return
    share_url = (
        f"https://t.me/share/url?url={url}"
        "&text=%E2%80%94%20__Pasted%20with__"
        "%20%F0%9F%A4%96%20%40ezpastebot"
    )
    reply = await m.reply_text(
        url,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Back to inline",
                        switch_inline_query=url
                    )
                ]
            ]
        ),
        quote=True
    )
    await m.reply_to_message.delete()
    await reply.edit_reply_markup(
        InlineKeyboardMarkup(
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
