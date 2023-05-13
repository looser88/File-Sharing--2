#(©)Codexbotz

import asyncio
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from plugins.link_generator import get_short
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
from datetime import datetime, timedelta

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
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    Slink = get_short(Tlink)
#   today= datetime.datetime.now()
    tomorrow = datetime.now() + timedelta(1)
#   ptoday= today.strftime("%d - %m - %Y")
    ptomorrow = tomorrow.strftime("%d - %m - %Y")
#   pweek = tomorrow.strftime("%A")
    media = message.video or message.document else: none 
    filename = media.file_name
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("AShare URL", url=Tlink)]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("BShare URL", url=Tlink)]])
    
        
    
    await reply_text.edit(f"{filename} \n▬▬▬▬▬▬▬ ❂ ▬▬▬▬▬▬▬▬</b>\n\n🗓𝐃𝐚𝐭𝐞:- <b>{ptomorrow}</b>\n\n      𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲 :- @Dot_serials_bot \n\n                     ⚜️⚜️⚜️⚜️⚜️⚜️\nᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :-\n{Slink}\n{Slink}\n\n     👇👇 𝐇𝐨𝐰 𝐭𝐨 𝐨𝐩𝐞𝐧 𝐥𝐢𝐧𝐤👇👇\nhttps://t.me/+Sb5ro1gyhgY0NWM1\nhttps://t.me/+Sb5ro1gyhgY0NWM1",disable_web_page_preview = True)
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    link = get_short(Tlink)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("CShare URL", url=Tlink)]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("DShare URL", url=Tlink)]])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
