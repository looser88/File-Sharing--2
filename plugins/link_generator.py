#(©)Codexbotz | Jigarvarma2005

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, SHORTLINK_URL, SHORTLINK_API
from helper_func import encode, get_message_id
import requests
import random
import string

def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars

def get_short(url):
    rget = requests.get(f"https://{SHORTLINK_URL}/api?api={SHORTLINK_API}&url={url}&alias={generate_random_alphanumeric()}")
    rjson = rget.json()
    if rjson["status"] == "success" or rget.status_code == 200:
        return rjson["shortenedUrl"]
    else:
        return url

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    Slink = get_short(Tlink)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=Slink)]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=Slink)]])
    
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{Tlink} \n\n<code>{Slink}</code>", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    Slink = get_short(Tlink)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=Tlink)]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=Tlink)]])
    
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n https://telegram.me/{client.username}?start={base64_string} \n{Tlink}\n<code>{link}</code>", quote=True, reply_markup=reply_markup)
