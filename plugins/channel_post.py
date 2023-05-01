#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from plugins.link_generator import get_short
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
import datetime

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = get_short(f"https://telegram.me/{client.username}?start={base64_string}")
    now = datetime.datetime.now()
    date = now.strftime("%d-%b-20%y")
    week = now.strftime("%a")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=link)]])

    await reply_text.edit(f"<b>     {date},{week}     /n/nPri᥎ᥲᴛᥱ ᥣiᥒκ 🔗</b>\n<code>https://telegram.me/{client.username}?start={base64_string}</code> \n\n<b>𐍃ɦ᧐rᴛ ᥣiᥒκ😎</b>\n<code>{link}</code>\n<code>{link}</code> ", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = get_short(f"https://telegram.me/{client.username}?start={base64_string}")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=link)]])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
