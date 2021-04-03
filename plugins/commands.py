from pyrogram import Client, filters, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.pastebin import ezpaste

reply_filter = filters.create(
    lambda
    _,
    __,
    m: m.reply_to_message and (
        m.reply_to_message.text or m.reply_to_message.document
    )
)


@Client.on_message(
    (filters.group | filters.private)
    & ~filters.edited
    & reply_filter
    & filters.regex('^\\/paste(@ezpastebot|)$')
)
async def paste(_, m: Message):
    reply = m.reply_to_message
    url = await ezpaste(reply)
    if not url:
        await m.reply_text("Invalid", quote=True)
        return
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


@Client.on_message(filters.private
                   & filters.regex('^\\/start$')
                   & ~filters.edited)
async def start(_, m: Message):
    await m.reply_text(
        f"{emoji.LABEL} **How to use this bot to upload paste to "
        "[ezpaste](https://ezup.dev/p)** "
        "(any of the following methods works):\n\n"
        "- Use in inline mode\n"
        "- send text or text file in private\n"
        "- reply to a text message or text file with /paste in private "
        "or groups (feel free to add this bot to your groups, it has "
        "privacy mode enabled so it does not read your chat history\n\n"
        "You can upload up to 1 megabytes of text on each paste",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Try inline",
                        switch_inline_query=""
                    )
                ]
            ]
        )
    )
