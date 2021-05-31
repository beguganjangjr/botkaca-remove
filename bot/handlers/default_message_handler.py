from pyrogram import Client, filters 
from pyrogram.types import Message
from bot import COMMAND
from bot.handlers import leech_handler
import time
import os
import tempfile


@Client.on_message(filters.private & ~filters.regex(r'^/') & ~filters.document)
async def func(client : Client, message : Message):
    message.text = "/" + COMMAND.LEECH + " " + message.text
    return await leech_handler.func(client, message)

@Client.on_message(filters.document & filters.private)
async def userVideo(client : Client, message : Message):
    link = None
    document = message.document
    if document.file_name.endswith('.torrent'):
        os.makedirs(str(message.from_user.id), exist_ok=True)
        fd, link = tempfile.mkstemp(dir=str(message.from_user.id), suffix='.torrent')
        os.fdopen(fd).close()
        await message.download(link)
        return await leech_handler.func(client, message)
    
        


    
    
