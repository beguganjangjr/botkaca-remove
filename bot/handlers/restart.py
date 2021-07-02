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
    #restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    #restart_message = await message.reply_text("Restarting, Please wait!")
    restart_message = await client.send_message(message.chat_id,
                                                reply_to_message_id=message.message_id,
                                                text="Restarting, Please wait!",
                                                parse_mode='HTMl')
    # Save restart message object in order to reply to it after restarting
    #await fs_utils.clean_all()
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    await fs_utils.clean_all()
    os.execl(executable, executable, "-m", "bot")
