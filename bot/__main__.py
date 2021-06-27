from pyrogram import filters, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot import CONFIG, COMMAND, LOCAL, LOGGER, STATUS
from bot.handlers import *
from bot.handlers import fs_utils
import asyncio
import shutil
import signal
import pickle
from os import execl, path, remove
from . import app

async def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        #restart_message.edit_text("Restarted Successfully!")
        #restart_message.edit_text("Restarted Successfully!")
        LOGGER.info('Restarted Successfully!')
        remove('restart.pickle')
        
    app.UPDATES_WORKERS = 100
    app.DOWNLOAD_WORKERS = 100
    app.set_parse_mode("html")
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
    await app.start()
    await idle()
    await app.stop()
    
if __name__ == "__main__":
    app.loop.run_until_complete(main())
