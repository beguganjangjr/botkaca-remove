from pyrogram import Client, filters 
from pyrogram.types import Message
from bot import COMMAND
from bot.handlers import leech_handler
import time
import os
import tempfile
import mimetypes

async def get_file_mimetype(filename):
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype:
        proc = await asyncio.create_subprocess_exec('file', '--brief', '--mime-type', filename, stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        mimetype = stdout.decode().strip()
    return mimetype or ''

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
        mimetype = await get_file_mimetype(link)
        return await leech_handler.func(client, message)
    
        


    
    
