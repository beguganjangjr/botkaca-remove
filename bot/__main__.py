from os.path import join as os_path_join
from pyrogram import Client, filters 
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


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        #restart_message.edit_text("Restarted Successfully!")
        #restart_message.edit_text("Restarted Successfully!")
        LOGGER.info('Restarted Successfully!')
        remove('restart.pickle')
        
    app = Client(
        ":memory:",
        bot_token=CONFIG.BOT_TOKEN,
        api_id=CONFIG.API_ID,
        api_hash=CONFIG.API_HASH,
        workers=32,
        workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR),
        plugins=dict(root="bot/handlers")
    )
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
    app.run()
    
if __name__ == "__main__":
    main()
