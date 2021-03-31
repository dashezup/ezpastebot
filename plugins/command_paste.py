from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.pastebin import ezpaste

reply_filter = filters.create(lambda _, __, m: m.reply_to_message)


@Client.on_message(
    (filters.group | filters.private)
    & ~filters.edited
    & reply_filter
    & filters.regex('^/paste$')
)
async def paste(_, m: Message):
    reply = m.reply_to_message
    if not reply or not reply.text:
        return
    url = await ezpaste(reply.text)
    share_url = (
        f"https://t.me/share/url?url={url}"
        "&text=%E2%80%94%20__Pasted%20with__"
        "%20%F0%9F%A4%96%20%40ezpastebot"
    )
    await reply.reply_text(
        url,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Share",
                        url=share_url
                    )
                ]
            ]
        ),
        quote=True
    )
