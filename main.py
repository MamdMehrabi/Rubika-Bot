from rubpy import Client, handlers, Message
from rubino import BaseMethod , Rubino
import asyncio
import sqlite3
import aiohttp


db = sqlite3.connect('rubika_bot.db')
cursor = db.cursor()

async def main():

    STEP = 'home'
    async with Client(session='rubpy') as app:
        @app.on(handlers.MessageUpdates())
        async def updates(message: Message):
            if message.raw_text == '/start':
                await message.reply(f"سلام کاربر {message.message_id}\n\nYour Guid: {message.author_object_guid}")
                try:
                    cursor.execute(
                        """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT , guid TEXT , types TEXT)"""
                    )
                    guid = message.author_object_guid
                    types = message.type
                    cursor.execute("INSERT INTO users(guid , types) VALUES(? , ?)" , (guid , types))
                    db.commit()
                except sqlite3.IntegrityError:
                    print("user id in sql!")
            if message.raw_text == '/help':
                await message.reply(f"این بات در جهت جواب دادن به سوالات شما با استفاده از هوش مصنوعی ساخته شده است...\nبرای استفاده از بات باید اول پیامتون gpt: بنویسید به عنوان مثال:\ngpt: سوالتون\nCreated By: @OnlyMamad\nJoin it in @TheLinux")
            if 'gpt:' in message.raw_text:
                text = message.raw_text[5:]
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'https://pyrubi.s70.xyz/chat.php/?text={text}') as response:
                        txt = await response.text()
                        txt = txt[25:-9]
                        await message.reply(txt)
            elif '/dl' in message.raw_text:
                link = message.raw_text[4:]
                client = Rubino("usfrcwvxmufqzwpfcmlywltmasowhgef")
                getProfile = client.getProfileList()['data']['profiles'][0]['id']
                dl = client.getPostByShareLink(link, getProfile)
                link_dl = dl['data']['post']['full_file_url']
                await message.reply(f"link for Download:\n{link_dl}\n\n@TheLinux and @OnlyMamad")
        await app.run_until_disconnected()

asyncio.run(main())