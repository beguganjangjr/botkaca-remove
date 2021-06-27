# GOAL:
# load config

import os
from bot.config import Config
import aiohttp
import requests

def liststring(string):
    kopyasiz = list(string.split(","))
    kopyasiz = list(dict.fromkeys(kopyasiz))
    return kopyasiz


def replacestring(string):
    string = string.replace("\n\n",",")
    string = string.replace("\n",",")
    string = string.replace(",,",",")
    string = string.rstrip(',')
    string = string.lstrip(',')
    return string


tracker_urlsss = [
    "https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt",
    "https://newtrackon.com/api/live"
    ]
trackers_list = ''
list_trackers = ''
for i in range(len(tracker_urlsss)):
    response = requests.get(tracker_urlsss[i])
    response.encoding = "utf-8"
    trackers_list += "\n"
    #response = response.text.strip()
    #response = response.replace("\n\n", ",")
    trackers_list += response.text
    
joinstring = liststring(replacestring(trackers_list))
trackers_list = ','.join(joinstring)
CONFIG = Config({
    'ROOT' : os.getcwd(),
    'WORKDIR' : 'sessions',
    'LOG_FILE' : 'log.txt',
    'MAX_LOG_SIZE' : 10 * 1024 * 1024,
    'API_HASH' : None,
    'API_ID' : None,
    'BOT_TOKEN' : None,
    'BOT_PASSWORD' : None,
    'CHAT_ID' : '',
    'EDIT_SLEEP' : 30,
    'UPLOAD_MAX_SIZE' : 2000 * 1024 * 1024,
    'UPLOAD_MIN_SIZE' : 100 * 1024,
    'UPLOAD_AS_DOC' : 0,
    'UPLOAD_AS_ZIP' : 0,
    'ARIA2_DIR' : 'downloads',
    'TORRENT_TRACKER' : f'{trackers_list}',
    'BAR_SIZE' : 10,
    'THUMBNAIL_NAME' : 'default_thumbnail.jpg',
    'LOCAL' : 'en',
    'PROXY' : None
})

# GOAL:
# prepare workdir

workdir = os.path.join(CONFIG.ROOT, CONFIG.WORKDIR)
if not os.path.isdir(workdir):
    os.mkdir(workdir)
del workdir

# GOAL:
# logging any important sign

logfile = os.path.join(CONFIG.ROOT, CONFIG.WORKDIR, CONFIG.LOG_FILE)

if os.path.exists(logfile):
    with open(logfile, "r+") as f_d:
        f_d.truncate(0)

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    #format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            logfile,
            maxBytes=CONFIG.MAX_LOG_SIZE,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# GOAL:
# Log configuration

LOGGER.info(dict(CONFIG))

del logfile

# GOAL:
# Localization

LOCAL = __import__(name = 'bot.locals.' + CONFIG.LOCAL, fromlist = ['LOCAL']).LOCAL

# GOAL:
# load Command format

COMMAND = Config({
    'START' : 'start',
    'PASSWORD' : 'pass',
    'HELP' : 'help',
    'LEECH' : 'leech',
    'RESTART' : 'restart',
    'CANCEL_LEECH' : 'cancel',
    'LEECH_LIST' : 'list',
    'UPLOAD_AS_DOC' : 'upload_as_doc',
    'UPLOAD_AS_ZIP' : 'upload_as_zip',
    'SET_THUMBNAIL' : 'set_thumbnail',
    'RESET_THUMBNAIL' : 'reset_thumbnail',
    'SET_TRACKER' : 'set_tracker'
}, 'COMMAND_')

# GOAL:
# set status

STATUS = type('obj', (object,), {
    'ARIA2_API' : None,
    'UPLOAD_AS_DOC' : bool(int(CONFIG.UPLOAD_AS_DOC)),
    'UPLOAD_AS_ZIP' : bool(int(CONFIG.UPLOAD_AS_ZIP)),
    'DEFAULT_TRACKER' : CONFIG.TORRENT_TRACKER.split(','),
    'CHAT_ID' : CONFIG.CHAT_ID.split(',')
})

app = Client(
        ':memory:',
        bot_token=CONFIG.BOT_TOKEN,
        api_id=CONFIG.API_ID,
        api_hash=CONFIG.API_HASH,
        workers=32,
        workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR),
        plugins=dict(root="bot/handlers"),
        parse_mode='html',
        sleep_threshold=30)
session = aiohttp.ClientSession()
