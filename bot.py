from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, date
import zoneinfo
from strings import *
from settings import *

zone = zoneinfo.ZoneInfo("Europe/Moscow")
app = Client("bot", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(posts_from))
async def on_new_message_1(client, message:Message):
    if date.today().weekday() > 4:
        return
    if datetime.now(zone).hour < 15 or datetime.now(zone).hour > 22:
        return
    text = ''
    file_id = None
    if message.text:
        text = message.text
    elif message.photo:
        if message.caption:
            text = message.caption
            file_id = message.photo.file_id
        else:
            await app.send_photo(send_to, message.photo.file_id)
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
        if file_id:
            await app.send_photo(send_to, file_id, text)
        else:
            await app.send_message(send_to, text)

app.run()