# GOAL:
# getting track for logging

import logging
import re
import urllib.parse
#import aiohttp
import requests
import os
LOGGER = logging.getLogger(__name__)

# GOAL:
# create /leech handler
from bs4 import BeautifulSoup

from re import match as re_match
from asyncio import sleep as asyncio_sleep
from os.path import join as os_path_join
from math import floor
from pyrogram import Client, filters 
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aria2p.downloads import Download, File
from bot import LOCAL, STATUS, CONFIG, COMMAND, session
from bot.plugins import aria2, zipfile
from bot.handlers import upload_to_tg_handler
from bot.handlers import cancel_leech_handler
from bot.plugins.exceptions import DirectDownloadLinkException
from bot.plugins.direct_link_generator import direct_link_generator
from functools import partial
#from bot.handlers.direct_link_generator import generate_directs

import asyncio
loop = asyncio.get_event_loop()
MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

def is_url(url: str):
    url = re.findall(URL_REGEX, url)
    if url:
        return True
    return False
def is_magnet(url: str):
    magnet = re.findall(MAGNET_REGEX, url)
    if magnet:
        return True
    return False

def is_torrent(file_name: str):
    if os.path.exists(file_name) and file_name.lower().endswith(".torrent"):
        return True
    return False


@Client.on_message(filters.command(COMMAND.LEECH))
async def func(client : Client, message: Message):
    mesg = message.text.split('\n')
    message_args = mesg[0].split(' ')
    name_args = mesg[0].split('|')
    proxy_args = mesg[0].split(',')
    try:
        link = message_args[1]
        print(link)
        if link.startswith("|") or link.startswith("pswd: "):
            link = ''
    except IndexError:
        link = ''
    try:
        name = name_args[1]
        name = name.strip()
        if name.startswith("pswd: "):
            name = ''
    except IndexError:
        name = ''
    try:
        proxy = proxy_args[1]
        proxy = proxy.strip()
    except IndexError:
        proxy = ''
    try:
        ussr = urllib.parse.quote(mesg[1], safe='')
        pssw = urllib.parse.quote(mesg[2], safe='')
    except:
        ussr = ''
        pssw = ''
    if ussr != '' and pssw != '':
        link = link.split("://", maxsplit=1)
        link = f'{link[0]}://{ussr}:{pssw}@{link[1]}'
    pswd = re.search('(?<=pswd: )(.*)', message.text)
    if pswd is not None:
      pswd = pswd.groups()
      pswd = " ".join(pswd)
    LOGGER.info(link)
    
    link = link.strip()
    timeout = 60
    referer = None
    proxies = None

    reply = await message.reply_text(LOCAL.ARIA2_CHECKING_LINK)
    reply_to = message.reply_to_message
    if reply_to is not None:
        file = None
        tag = reply_to.from_user.username
        media_array = [reply_to.document, reply_to.video, reply_to.audio]
        for i in media_array:
            if i is not None:
                file = i
                break

        if not is_url(link) and not is_magnet(link) or len(link) == 0:
            if file is not None:
                if file.mime_type != "application/x-bittorrent":
                    await reply.edit_text('No download source provided / No torrent file detected')
                    return
                else:
                    link = await reply_to.download()
                    LOGGER.info(link)
    else:
        tag = None
    if not is_url(link) and not is_magnet(link):
        await reply.edit_text('No download source provided')
        return
    
    try:
        link = await direct_link_generator(link)
        if 'dood' in link:
            if CONFIG.PROXY is not None:
                proxies = 'http://{0}'.format(CONFIG.PROXY)
                referer = '*'
            else:
                referer = '*'
                proxies = 'http://{0}'.format(proxy)
    except DirectDownloadLinkException as e:
        LOGGER.info(f'{link}: {e}')
        if "ERROR:" in str(e):
            await reply.edit_text(
                str(e)
            )
            return

    
    #await asyncio_sleep(1)   

    #elif CONFIG.PROXY is not None:
        #proxy = 'http://{0}'.format(CONFIG.PROXY)   
    
    download_dir = os_path_join(CONFIG.ROOT, CONFIG.ARIA2_DIR)
    STATUS.ARIA2_API = STATUS.ARIA2_API or aria2.aria2(
        config={
            'dir' : download_dir
            
        }
    )
    aria2_api = STATUS.ARIA2_API
    await asyncio_sleep(1)
    await aria2_api.start()
    LOGGER.debug(f'Leeching : {link}')
    LOGGER.info(f'Leeching : {link}') 
    LOGGER.info(f'proxy: {proxy}')
    try:
        if is_magnet(link):
            download = await loop.run_in_executor(None, partial(aria2_api.add_magnet, link, options={
                'continue_downloads' : True,
                'bt_tracker' : STATUS.DEFAULT_TRACKER}))
            
        elif is_torrent(link):
            download = await loop.run_in_executor(None, partial(aria2_api.add_torrent, link, options={
                'follow-torrent': True,
                'bt_tracker' : STATUS.DEFAULT_TRACKER}))
            
        else:
             download = await loop.run_in_executor(None, partial(aria2_api.add_uris, [link], options={
                 'continue_downloads' : True,
                 'all-proxy': proxies,
                 'referer': referer,
                 'check-certificate': False,
                 #'http-no-cache': _cache,
                 'follow-torrent': False,
                 #'timeout': timeout,
                 'connect-timeout': timeout,
                 'out': name}))
             

    except Exception as e:
        if "No URI" in str(e):
            await reply.edit_text(
                LOCAL.ARIA2_NO_URI
            )
            return
        else:
            LOGGER.error(str(e))
            await reply.edit_text(
                str(e)
            )
            return

    if await progress_dl(reply, aria2_api, download.gid):
        download = aria2_api.get_download(download.gid)
        if not download.followed_by_ids:
            download.remove(force=True)
            await upload_files(client, reply, abs_files(download_dir, download.files), os_path_join(download_dir, download.name + '.zip'))
        else:
            gids = download.followed_by_ids
            download.remove(force=True, files=True)
            for gid in gids:
                if await progress_dl(reply, aria2_api, gid):
                    download = aria2_api.get_download(gid)
                    download.remove(force=True)
                    await upload_files(client, reply, abs_files(download_dir, download.files), os_path_join(download_dir, download.name + '.zip'))
        try:
            await reply.delete()
        except:
            pass

def abs_files(root, files):
    def join(file):
        return os_path_join(root, file.path)
    return map(join, files)

async def upload_files(client, reply, filepaths, zippath):
    if not STATUS.UPLOAD_AS_ZIP:
        for filepath in filepaths:
            await upload_to_tg_handler.func(
                filepath,
                client,
                reply,
                delete=True
            )
    else:
        zipfile.func(filepaths, zippath)
        await upload_to_tg_handler.func(
            zippath,
            client,
            reply,
            delete=True
        )

async def progress_dl(message : Message, aria2_api : aria2.aria2, gid : int, previous_text=None):
    try:
        download = aria2_api.get_download(gid)
        if not download.is_complete:
            if not download.error_message:
                block = ""
                for i in range(1, int(CONFIG.BAR_SIZE) + 1):
                    if i <= floor(download.progress * int(CONFIG.BAR_SIZE)/100):
                        block += LOCAL.BLOCK_FILLED
                    else:
                        block += LOCAL.BLOCK_EMPTY
                text = LOCAL.ARIA2_DOWNLOAD_STATUS.format(
                    name = download.name,
                    block = block,
                    percentage = download.progress_string(),
                    total_size = download.total_length_string(),
                    download_speed = download.download_speed_string(),
                    upload_speed = download.upload_speed_string(),
                    seeder = download.num_seeders if download.is_torrent else 1,
                    eta = download.eta_string(),
                    gid = download.gid
                )
                if text != previous_text:
                    await message.edit(
                        text,
                        reply_markup=
                            InlineKeyboardMarkup([[
                                InlineKeyboardButton(
                                    COMMAND.CANCEL_LEECH,
                                    callback_data=COMMAND.CANCEL_LEECH + " " + download.gid,
                                    
                                )
                            ]])
                    )
                await asyncio_sleep(int(CONFIG.EDIT_SLEEP))
                return await progress_dl(message, aria2_api, gid, text)
            else:
                await message.edit(download.error_message)
        else:
            await message.edit(
                LOCAL.ARIA2_DOWNLOAD_SUCCESS.format(
                    name=download.name
                )
            )
            return True
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await message.delete()
            return False
        elif " depth exceeded" in str(e):
            download.remove(force=True)
            await message.edit(
                LOCAL.ARIA2_DEAD_LINK.format(
                    name = download.name
                )
            )
            return False
        else:
            LOGGER.exception(str(e))
            await message.edit("<u>error</u> :\n<code>{}</code>".format(str(e)))
            return False
