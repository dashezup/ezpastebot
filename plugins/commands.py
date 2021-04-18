import asyncio
from pyrogram import Client, filters, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.pastebin import ezpaste

DELETE_DELAY = 6


async def _delay_delete_message(m: Message):
    await asyncio.sleep(DELETE_DELAY)
    await m.delete()


@Client.on_message(
    (filters.group | filters.private)
    & ~filters.edited
    & filters.regex('^\\/paste(@ezpastebot|)$')
)
async def paste(_, m: Message):
    reply = m.reply_to_message
    valid_input = reply and (reply.text or reply.document)
    if not valid_input:
        response = await m.reply_text(
            "Reply to a text message/file with the command to "
            "upload to [ezpaste](https://ezup.dev/p/)",
            quote=True,
            disable_web_page_preview=True
        )
        await _delay_delete_message(response)
        return
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
                    ),
                    InlineKeyboardButton(
                        "Inline",
                        switch_inline_query=url
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
        "You can upload up to 1 megabytes of text on each paste\n\n"
        "[Source Code](https://github.com/dashezup/ezpastebot)"
        " | [Developer](https://t.me/dashezup)"
        " | [Support Chat](https://t.me/ezupdev)",
        disable_web_page_preview=True,
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
