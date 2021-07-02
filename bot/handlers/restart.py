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
from bot.handlers.fs_utils import *

@Client.on_message(filters.command(COMMAND.RESTART))
async def restart(client: Client, message: Message):
    restart_message = await sendMessage("Restarting, Please wait!", client, message)
    chat_id = restart_message.chat.id
    msg_id = restart_message.message_id
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{chat_id}\n{msg_id}\n")
    await fs_utils.clean_all()
    os.execl(executable, executable, "-m", "bot")
