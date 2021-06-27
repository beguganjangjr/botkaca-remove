import sys
import shutil
import os
import pathlib
import tarfile
from os.path import join as os_path_join
from bot import STATUS, CONFIG
from bot.plugins import aria2
from pyrogram import Client
from pyrogram.types import Message
from bot import app

workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR)

async def editMessage(text: str, message: Message, reply_markup=None):
    try:
        app.edit_message_text(text=text, message_id=message.message_id,
                              chat_id=message.chat.id,reply_markup=reply_markup,
                              parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))
        
        
async def sendMessage(text: str, client: Client, message: Message):
    try:
        return await client.send_message(chat_id=message.chat.id,
                            reply_to_message_id=message.message_id,
                            text=text)
    except Exception as e:
        LOGGER.error(str(e))
        
        
def start_cleanup():
    try:
        shutil.rmtree(workdir)
    except FileNotFoundError:
        pass

async def clean_all():
    STATUS.ARIA2_API = STATUS.ARIA2_API or aria2.aria2(
        config={
            'dir' : dir
        }
    )
    aria2_api = STATUS.ARIA2_API
    await aria2_api.start()
    aria2_api.remove_all(True)
    try:
        shutil.rmtree(workdir)
    except FileNotFoundError:
        pass

def exit_clean_up(signal, frame):
    try:
        LOGGER.info("Please wait, while we clean up the downloads and stop running downloads")
        clean_all()
        sys.exit(0)
    except KeyboardInterrupt:
        LOGGER.warning("Force Exiting before the cleanup finishes!")
        sys.exit(1)
