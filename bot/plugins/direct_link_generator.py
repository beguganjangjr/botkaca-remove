# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

import aiohttp
import asyncio
import logging
import json
import random
import time
import re
import string
import urllib.parse
from os import popen
from random import choice
import lk21
import logging
import requests
from bs4 import BeautifulSoup
from bot import CONFIG, PROXY
from bot.plugins.exceptions import DirectDownloadLinkException
from bot.plugins import jsunpack
from js2py import EvalJs
from getuseragent import UserAgent
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
LOGGER = logging.getLogger(__name__)    
ua = UserAgent()
loop = asyncio.get_event_loop()

def get_proxy() -> str:
    '''
    Get proxy (str) from API.
    '''
    proxy = requests.get(PROXY).text
    return proxy.rstrip()        

async def direct_link_generator(link: str):
    """ direct links generator """
    if not link:
        raise DirectDownloadLinkException("`No links found!`")
    elif 'youtube.com' in link or 'youtu.be' in link:
        raise DirectDownloadLinkException("YT DL Unsupported Yet")
    elif 'drive.google.com' in link:
        raise DirectDownloadLinkException("No Support Mirrorring GDRIVE link")
    elif 'zippyshare.com' in link:
        return zippy_share(link)
    elif 'yadi.sk' in link:
        return yandex_disk(link)
    elif 'cloud.mail.ru' in link:
        return cm_ru(link)
    elif 'mediafire.com' in link:
        return mediafire(link)
    elif 'osdn.net' in link:
        return osdn(link)
    elif 'github.com' in link:
        return github(link)
    #elif 'hxfile.co' in link:
    #    return hxfile(link)
    elif 'anonfiles.com' in link:
        return anon(link)
    elif 'letsupload.io' in link:
        return letsupload(link)
    elif 'fembed.com' in link:
        return fembed(link)
    elif 'femax20.com' in link:
        return fembed(link)
    elif 'feurl.com' in link:
        return fembed(link)
    elif 'naniplay.nanime.in' in link:
        return fembed(link)
    elif 'naniplay.nanime.biz' in link:
        return fembed(link)
    elif 'naniplay.com' in link:
        return fembed(link)
    elif 'layarkacaxxi.icu' in link:
        return fembed(link)
    elif 'sbembed.com' in link:
        return sbembed(link)
    elif 'streamsb.net' in link:
        return sbembed(link)
    elif '1drv.ms' in link:
        return onedrive(link)
    elif 'pixeldrain.com' in link:
        return pixeldrain(link)
    elif 'racaty.net' in link or 'hxfile.co' in link or 'files.im' in link:
        return filesim_(link)
    elif 'streamtape.com' in link:
        return await streamtape(link)
    elif 'mixdrop' in link:
        return await mixdrop(link)
    elif 'dood.la' in link \
        or 'dood.so' in link \
        or 'dood.cx' in link \
        or 'dood.to' in link:
            return await dood(link)
    else:
        raise DirectDownloadLinkException(f'No Direct link function found for {link}')


        

def filesim_(url: str) -> str:
    """ Anonfiles direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\b(https?://.*(files|racaty|hxfile)*(|com|net|im)\S+)', url)[0][0]
    except IndexError:
        raise DirectDownloadLinkException("`No Hxfile / racaty / files.im links found`\n")
    bypasser = lk21.Bypass()
    LOGGER.info(link)
    dl_url = bypasser.bypass_url(link)
    return dl_url
        
    
        
def zippy_share(url: str) -> str:
    """ ZippyShare direct links generator
    Based on https://github.com/KenHV/Mirror-Bot """
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, 'html.parser')

    try:
        js_script = bs_obj.find("div", {"class": "center",}).find_all(
            "script"
        )[1]
    except:
        js_script = bs_obj.find("div", {"class": "right",}).find_all(
            "script"
        )[0]

    js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
    js_content = 'var x = "/' + js_content[0] + '"'

    evaljs = EvalJs()
    setattr(evaljs, "x", None)
    evaljs.execute(js_content)
    js_content = getattr(evaljs, "x")

    return f"https://{link}.zippyshare.com{js_content}"

def zippy_share_(url: str) -> str:
    dl_url = ''
    try:
        link = re.findall("https:/.(.*?).zippyshare", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Zippyshare links found`\n")
        
    bypasser = lk21.Bypass()
    try:
        dl_url=bypasser.bypass_url(link)
    except:
        dl_url = bypasser.bypass_fembed(link)
#        raise DirectDownloadLinkException("`ERROR extracting Link`\n")
    return dl_url        
    
def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct """
    try:
        link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(link)).json()['href']
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: File not found/Download limit reached`\n")


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py """
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*cloud\.mail\.ru\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No cloud.mail.ru links found`\n")
    command = f'vendor/cmrudl.py/cmrudl -s {link}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
    dl_url = data['download']
    return dl_url


def uptobox(url: str) -> str:
    """ Uptobox direct links generator
    based on https://github.com/jovanzers/WinTenCermin """
    try:
        link = re.findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Uptobox links found`\n")
    if UPTOBOX_TOKEN is None:
        logging.error('UPTOBOX_TOKEN not provided!')
        dl_url = url
    else:
        try:
            link = re.findall(r'\bhttp?://.*uptobox\.com/dl\S+', url)[0]
            logging.info('Uptobox direct link')
            dl_url = url
        except:
            file_id = re.findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
            file_link = 'https://uptobox.com/api/link?token=%s&file_code=%s' % (UPTOBOX_TOKEN, file_id)
            req = requests.get(file_link)
            result = req.json()
            dl_url = result['data']['dlLink']
    return dl_url


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url        



def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = 'https://osdn.net'
    try:
        link = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No OSDN links found`\n")
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'html.parser')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    urls = []
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        urls.append(re.sub(r'm=(.*)&f', f'm={mirror}&f', link))
    return urls[0]


def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No GitHub Releases links found`\n")
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")


def hxfile(url: str) -> str:
    """ Hxfile direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*hxfile\.co\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Hxfile links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def anon(url: str) -> str:
    """ Anonfiles direct links generator
    based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*anonfiles\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Anonfiles links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def letsupload(url: str) -> str:
    """ Letsupload direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*letsupload\.io\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Letsupload links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def fembed(link: str) -> str:
    """ Fembed direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_fembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def sbembed(link: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_sbembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def streamtape_(url: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/breakdowns/slam-mirrorbot """
    dl_url= '' 
    try:
        link = re.findall(r'\bhttps?://.*streamtape\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No streamtape links found`\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_streamtape(link)
    return dl_url


def onedrive(link: str) -> str:
    """ Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge """
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    return dl_link


def pixeldrain(url: str) -> str:
    """ Based on https://github.com/yash-dk/TorToolkit-Telegram """
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
    dl_link = f"https://pixeldrain.com/api/file/{file_id}"
    resp = requests.get(info_link).json()
    if resp["success"]:
        return dl_link
    else:
        raise DirectDownloadLinkException("ERROR: Cant't download due {}.".format(resp.text["value"]))
        
        
        
        
async def mixdrop(url: str) -> str:
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*mixdrop\.(?:co|to|sx)/(?:f|e)\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Mixdrop links found`\n")
    web_url = re.findall(r'(?://|\.)(mixdrop\.(?:co|to|sx))/(?:f|e)/(\w+)', url)[0]
    media_id = web_url[1]
    host = web_url[0]
    link = link.replace('/f/','/e/')
    user_agent = ua.Random()
    headers = {'Origin': 'https://{}'.format(host),
               'Referer': 'https://{}/'.format(host),
               'User-Agent': user_agent}
    #proxies = 'http://{0}'.format(proxy)
    session_timeout = aiohttp.ClientTimeout(total=None)
    try:
        #async with aiohttp.ClientSession() as ses:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url=link, headers=headers, timeout=None) as response:
                if response.status != 200:
                    LOGGER.error(f'Response status: {response.status}')
                else:
                    d_content = await response.text()
                        
    except aiohttp.client_exceptions.ClientConnectorError as e:
        raise DirectDownloadLinkException(str(e))
    except aiohttp.ContentTypeError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
    r = re.search(r'location\s*=\s*"([^"]+)', d_content)
    if r:
        link = 'https://{0}{1}'.format(host, r.group(1))
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url=link, headers=headers) as response:
                if response.status != 200:
                    LOGGER.error(f'Response status: {response.status}')
                else:
                    d_content = await response.text()
                    
    if '(p,a,c,k,e,d)' in d_content:
        d_content = get_packed_data(d_content)
            
    r = re.search(r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)', d_content)
    if r:
        headers = {'User-Agent': user_agent, 'Referer': link}
        dl_url = "https:" + r.group(1) + append_headers(headers)
            #dl_url = "https:" + r.group(1)
        return dl_url
    raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
      
async def streamtape(url: str) -> str:
    dl_url= ''       
    try:
        link = re.findall(r'\bhttps?://.*streamtape\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No streamtape links found`\n")
    web_url = re.findall(r'(?://|\.)(streamtape\.com)/(?:e|v)/([0-9a-zA-Z]+)', link)[0]    
    media_id = web_url[1]
    host = web_url[0]
    user_agent = ua.Random()
    #link = 'https://' + host + '/v/' + media_id
    headers = {'User-Agent': user_agent,
               'Referer': 'https://{0}/'.format(host)}
    session_timeout = aiohttp.ClientTimeout(total=None)
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url=link, headers=headers, timeout=None) as response:
            d_content = await response.text()
    src = re.search(r'''ById\('vi.+?=\s*["']([^"']+)['"].+?["']([^"']+)''', d_content)
    if src:
        src_url = 'https:{0}{1}&stream=1'.format(src.group(1), src.group(2))
        dl_url = get_redirect_url(src_url, headers) + append_headers(headers)
        return dl_url
    raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
                
async def dood(url: str) -> str:
    pattern = re.compile("\\d{1,3}(?:\\.\\d{1,3}){3}(?::\\d{1,5})?")
    web_url = re.findall(r'(?://|\.)(dood(?:stream)?\.(?:com|watch|to|so|cx|la))/(?:d|e)/([0-9a-zA-Z]+)', url)[0]
    proxy = re.findall(pattern, url)[0]
    media_id = web_url[1]
    host = web_url[0]
    link = 'https://' + host + '/e/' + media_id
    user_agent = ua.Random()
    headers = {'User-Agent': user_agent,
               'Referer': 'https://{0}/'.format(host)}
        #link.replace('/d/','/e/')
    proxies = 'http://{0}'.format(proxy)
    session_timeout = aiohttp.ClientTimeout(total=None)
    try:
        async with aiohttp.ClientSession(trust_env=True, timeout=session_timeout) as ses:
            async with ses.get(url=link, headers=headers, proxy=proxies, timeout=None) as response:
                if response.status != 200:
                    LOGGER.error(f'Response status: {response.status}')
                else:
                    text = await response.text()
    except aiohttp.client_exceptions.ClientConnectorError as e:
        LOGGER.error(f'Cannot connect to mixdrop: {e}')
        raise DirectDownloadLinkException(str(e))
     
    except aiohttp.ContentTypeError:
        LOGGER.error('decode failed')
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
            
           
        #LOGGER.info(f'text: {text}')
    match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', text, re.DOTALL)
    if match:
        token = match.group(2)
        url = 'https://{0}{1}'.format(host, match.group(1))
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url=url, headers=headers, proxy=proxies) as response:
                html = await response.text()
                #response = await ses.get(url=url, headers=headers, proxy=proxies)
                #html = await response.text()
                dl_url = dood_decode(html) + token + str(int(time.time() * 1000)) + append_headers(headers)
                #LOGGER.info(f'dl_url: {dl_url}')
                return dl_url
    raise DirectDownloadLinkException("`Error: Can't extract the link`\n")

def get_redirect_url(url, headers={}):
    request = urllib.request.Request(url, headers=headers)
    request.get_method = lambda: 'HEAD'
    response = urllib.request.urlopen(request)
    return response.geturl()


def get_packed_data(html):
    packed_data = ''
    for match in re.finditer(r'(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        if jsunpack.detect(match.group(1)):
            packed_data += jsunpack.unpack(match.group(1))

    return packed_data

def dood_decode(data):
    t = string.ascii_letters + string.digits
    return data + ''.join([random.choice(t) for _ in range(10)])


def append_headers(headers):
    headers = '|%s' % '&'.join(['%s=%s' % (key, urllib.parse.quote_plus(headers[key])) for key in headers])
    return headers

