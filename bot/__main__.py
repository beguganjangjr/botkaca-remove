from pyrogram import filters, idle, Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot import CONFIG, COMMAND, LOCAL, LOGGER, STATUS
from bot.handlers import *
from bot.handlers import fs_utils
import asyncio
import shutil
import signal
import pickle
import traceback
from os import execl, path, remove
from . import app
import os

async def main():    
    #async def _autorestart_worker():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    await app.start()
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        await app.edit_text("Restarted successfully!", chat_id, msg_id)
        os.remove(".restartmsg")   

                        
    #asyncio.create_task(_autorestart_worker())   
    app.UPDATES_WORKERS = 100
    app.DOWNLOAD_WORKERS = 100
    #app.set_parse_mode("html")
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)
    # register /start handler
    app.add_handler(
        MessageHandler(
            start_message_handler.func,
            filters=filters.command(COMMAND.START)
        )
    )

    if CONFIG.BOT_PASSWORD:
        # register /pass handler
        app.add_handler(
            MessageHandler(
                password_handler.func,
                filters = filters.command(COMMAND.PASSWORD)
            )
        )

        # take action on unauthorized chat room
        app.add_handler(
            MessageHandler(
                wrong_room_handler.func,
                filters = lambda msg: not msg.chat.id in STATUS.CHAT_ID
            )
        )
    #await app.start()
    await idle()
    await app.stop()
if __name__ == "__main__":
    app.loop.run_until_complete(main())
