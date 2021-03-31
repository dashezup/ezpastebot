from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.private
                   & filters.regex('^/start$')
                   & ~filters.edited)
async def start(_, m: Message):
    await m.reply_text(
        "ezpaste, upload your paste to https://ezup.dev/p\n\n"
        "Send text to paste or reply to a message with /paste,"
        "you can also add the bot to a group and use /paste command",
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
