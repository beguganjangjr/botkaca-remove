import pickle
from bot import LOCAL, CONFIG, STATUS, COMMAND
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from os import execl
from sys import executable
from bot.handlers import fs_utils

@Client.on_message(filters.command(COMMAND.RESTART))
async def restart(client: Client, message: Message):
    restart_message = await message.reply_text(
        "Restarting, Please wait!")
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")
