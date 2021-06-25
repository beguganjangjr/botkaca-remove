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
#def restart(client: Client, message: Message):
    #restart_message = sendMessage(
    #    "Restarting, Please wait!",
    #    client,
    #    message
    #)
#    restart_message = message.reply_text("Restarting, Please wait!")
#    # Save restart message object in order to reply to it after restarting
##    fs_utils.clean_all()
 #   with open('restart.pickle', 'wb') as status:
 #       pickle.dump(restart_message, status)
 #       status.close()
 #   execl(executable, executable, "-m", "bot")
def restart(client: Client, message: Message):
    restart_message = sendMessage("Restarting, Please wait!", client, message)
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    os.execl(executable, executable, "-m", "bot")
