from pyrogram import Client, filters 
from pyrogram.types import Message
from bot import COMMAND
from bot.handlers import leech_handler
import time

@Client.on_message(filters.private & ~filters.regex(r'^/'))
async def func(client : Client, message : Message):
    message.text = "/" + COMMAND.LEECH + " " + message.text
    return await leech_handler.func(client, message)

@Client.on_message(filters.document & filters.private)
async def userVideo(client : Client, message : Message):
    file = message.document
    link = file.get_file().file_path
    return await leech_handler.func(client, message)
    
    
