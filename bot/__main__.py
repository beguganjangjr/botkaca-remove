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
import traceback
from os import execl, path, remove
from . import app
preserved_logs = []
async def main():
    async def _autorestart_worker():
        while True:
            try:
                await app.send_message(1741587120, 'BOT STARTED')
            except Exception as ex:
                preserved_logs.append(ex)
                logging.exception('upload worker commited suicide')
                tb = traceback.format_exc()
                for i in STATUS.CHAT_ID:
                    try:
                        await app.send_message(i, 'upload worker commited suicide')
                        await app.send_message(i, tb, parse_mode=None)
                    except Exception:
                        logging.exception('failed %s', i)
                        tb = traceback.format_exc()
                        
    asyncio.create_task(_autorestart_worker())   
    app.UPDATES_WORKERS = 100
    app.DOWNLOAD_WORKERS = 100
    app.set_parse_mode("html")
    LOGGER.info("Bot Started!")
    await app.send_message(1741587120, 'BOT STARTED')
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
