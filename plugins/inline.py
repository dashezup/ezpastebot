from pyrogram import Client, filters
from pyrogram.types import (InlineQuery, Message,
                            InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            InlineQueryResultPhoto,
                            ForceReply)
from utils.pastebin import ezpaste

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
        url = query
        url_raw = f"{query}/index.txt"
        paste_id = url[19:]
        paste_info = f"ezpaste: [{paste_id}]({url}) | [raw]({url_raw})"
        share_url = (
            f"https://t.me/share/url?url={url}"
            "&text=%E2%80%94%20__Pasted%20with__"
            "%20%F0%9F%A4%96%20%40ezpastebot"
        )
        preview_image_url = f"{url}/preview.png"
        await iq.answer(
            results=[
                InlineQueryResultArticle(
                    title="Send URL of this paste",
                    input_message_content=InputTextMessageContent(
                        paste_info
                    ),
                    url=url,
                    description="A paste on ezup.dev/p",
                    thumb_url=preview_image_url,
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
                ),
                InlineQueryResultPhoto(
                    photo_url=preview_image_url,
                    thumb_url=preview_image_url,
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
            ],
            cache_time=1
        )
        return
    await iq.answer(
        results=[],
        cache_time=1,
        switch_pm_text="Send paste in PM",
        switch_pm_parameter="from_inline"
    )


@Client.on_message(filters.private & filters.regex('^/start from_inline$'))
async def receive_private_message(_, m: Message):
    await m.reply_text(ASK_TO_SEND_PASTE, reply_markup=ForceReply())


@Client.on_message(filters.private & answer_with_paste)
async def reply_with_text(_, m: Message):
    url = await ezpaste(m)
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
                    )
                ]
            ]
        )
    )
