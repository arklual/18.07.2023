from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, date
import zoneinfo
from strings import *
from settings import *
import os

zone = zoneinfo.ZoneInfo("Europe/Moscow")
app = Client("bot", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(posts_from))
async def on_new_message_1(client, message:Message):
    if date.today().weekday() > 4:
        return
    if datetime.now(zone).hour < 13 or datetime.now(zone).hour > 22:
        return
    text = ''
    file_id = None
    file_path = None
    if message.text:
        text = message.text
    elif message.photo:
        if message.caption:
            text = message.caption
            file_path = await app.download_media(message.photo.file_id)
        else:
            file_path = await app.download_media(message.photo.file_id)
            with open(file_path, 'rb') as f:
                await app.send_photo(send_to, f)
            os.remove(file_path)
            return

    if '+' in text.lower():
        with open('1.jpg', 'rb') as f:
            await app.send_photo(send_to, f, '+')
    elif 'около 15:00' in text.lower():
        await app.send_message(send_to, FIFTEEN_MESSAGE)
    elif 'первую сессию' in text.lower():
        await app.send_message(send_to, FIRSTSES_MESSAGE)
    elif 'закончим торговлю' in text.lower():
        await app.send_message(send_to, FINISH_MESSAGE)
    else:
        if file_path:
            with open(file_path, 'rb') as f:
                await app.send_photo(send_to, f)
            os.remove(file_path)
        else:
            await app.send_message(send_to, text)

app.run()
