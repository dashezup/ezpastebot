from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from utils.pastebin import ezpaste

reply_filter = filters.create(lambda _, __, m: m.reply_to_message)


@Client.on_message(filters.private & ~reply_filter & ~filters.regex("^/"))
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


@Client.on_callback_query(filters.regex("^yes_upload_paste"))
async def upload_paste(_, cq: CallbackQuery):
    url = await ezpaste(cq.message.reply_to_message.text)
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
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("^ignore"))
async def ignore(_, cq: CallbackQuery):
    await cq.message.delete()
