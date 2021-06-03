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


    
        


    
    
