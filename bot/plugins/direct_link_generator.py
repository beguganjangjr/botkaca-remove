# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

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
from bot import CONFIG
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
ua = ua.Random()

async def direct_link_generator(link: str, proxy):
    """ direct links generator """
    if not link:
        raise DirectDownloadLinkException("`No links found!`")
    elif 'youtube.com' in link or 'youtu.be' in link:
        raise DirectDownloadLinkException(f"Youtube Link use /{BotCommands.WatchCommand} or /{BotCommands.TarWatchCommand}")
    elif 'drive.google.com' in link:
        raise DirectDownloadLinkException(f"G-Drive Link use /{BotCommands.CloneCommand}")
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
    elif 'hxfile.co' in link:
        return hxfile(link)
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
    elif 'streamtape.com' in link:
        return streamtape(link)
    elif 'mixdrop' in link:
        return mixdrop(link)
    elif 'dood.la' in link \
        or 'dood.so' in link \
        or 'dood.cx' in link \
        or 'dood.to' in link:
            return dood(link, proxy)
    else:
        raise DirectDownloadLinkException(f'No Direct link function found for {link}')


def zippy_share(url: str) -> str:
    """ ZippyShare direct links generator
    Based on https://github.com/KenHV/Mirror-Bot """
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, "html.parser")

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


def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
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
        raise DirectDownloadLinkException("`Error: File not found / Download limit reached`\n")


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
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


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    page = BeautifulSoup(requests.get(link).content, 'html.parser')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
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


def streamtape(url: str) -> str:
    """ streamtape direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*streamtape\.com\S+', url)[0]
        media_id = link[1]
        host = link[0]
        user_agent = ua
        headers = {'User-Agent': user_agent,
                   'Referer': 'https://{0}/'.format(host)}
        rcontent = requests.get(url, headers=headers).content
        d_content = rcontent.decode("utf-8") 
        src = re.search(r'''ById\('vi.+?=\s*["']([^"']+)['"].+?["']([^"']+)''', d_content)
        header_2 = '|%s' % '&'.join(['%s=%s' % (key, urllib.parse.quote_plus(headers[key])) for key in headers])
        if src:
            src_url = 'https:{0}{1}&stream=1'.format(src.group(1), src.group(2))
            dl_url = get_redirect_url(src_url, headers) + append_headers(headers)
            return dl_url
    except IndexError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
        
        
def doodi(url: str) -> str:
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                LOGGER.info(chunk)
        with open(local_filename, 'r') as f:
            text = f.read()
            LOGGER.info(text)
    match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', local_filename, re.DOTALL)
    if match:
        token = match.group(2)
        url = 'https://{0}{1}'.format(host, match.group(1))
        html = requests.get(url, headers=headers).content.decode('utf-8')
        dl_url = dood_decode(html) + token + str(int(time.time() * 1000)) + append_headers(headers)
        return dl_url
    else:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")


   # """ doodstream direct links generator
   # based on https://github.com/breakdowns/slam-mirrorbot """
   # dl_url = ''
   # try:
   ##     link = re.findall(r'\bhttps?://.*dood\.(?:com|watch|to|so|cx|la)\S+', url)[0]
    #except IndexError:
    ##    raise DirectDownloadLinkException("`No Anonfiles links found`\n")
    #bypasser = lk21.Bypass()
    #dl_url=bypasser.bypass_url(link)
    #return dl_url        


def dood(url: str, proxy) -> str:
    """ dood direct links generator """
    web_url = re.findall(r'(?://|\.)(dood(?:stream)?\.(?:com|watch|to|so|cx|la))/(?:d|e)/([0-9a-zA-Z]+)', url)[0]
    media_id = web_url[1]
    host = web_url[0]
    #LOGGER.info(f"{host}{media_id}")
    link = 'https://' + host + '/e/' + media_id
    headers = {'User-Agent': ua,
               'Referer': 'https://{0}/'.format(host)}
    link.replace('/d/','/e/')
    #LOGGER.info(link)
    proxies = {'https': 'http://{0}'.format(proxy)}
    session = requests.Session()
    session.proxies.update(proxies)
    html = session.get(link, headers=headers, timeout=None).content
    text = html.decode('utf-8')
    #response = session.get(link).text
    LOGGER.info(f'proxy: {proxies}')
    match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', text, re.DOTALL)
    if match:
        token = match.group(2)
        url = 'https://{0}{1}'.format(host, match.group(1))
        html = session.get(url, headers=headers).content.decode('utf-8')
        dl_url = dood_decode(html) + token + str(int(time.time() * 1000)) + append_headers(headers)
        #dl_url = dl_url.split('|')[0]
        #LOGGER.info(f'dl_url: {dl_url}')
        return dl_url    
    raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
        
        
        
def mixdrop(url: str) -> str:
    """ mixdrop direct links generator """
    web_url = re.findall(r'(?://|\.)(mixdrop\.(?:co|to|sx))/(?:f|e)/(\w+)', url)[0]
    media_id = web_url[1]
    host = web_url[0]
    link = 'https://' + host + '/e/' + media_id
    LOGGER.info(f'dl_gen_link: {link}')
    user_agent = ua
    
    headers = {'Origin': 'https://{}'.format(host),
               'Referer': 'https://{}/'.format(host),
               'User-Agent': user_agent}
    rcontent = requests.get(link, headers=headers).content
    d_content = rcontent.decode("utf-8") 
    r = re.search(r'location\s*=\s*"([^"]+)', d_content)
    header_2 = '|%s' % '&'.join(['%s=%s' % (key, urllib.parse.quote_plus(headers[key])) for key in headers])
    if r:
        url = 'https://{0}{1}'.format(host, r.group(1))
        d_content = requests.get(link, headers=headers).content.decode("utf-8")
    if '(p,a,c,k,e,d)' in d_content:
        d_content = get_packed_data(d_content)
    r = re.search(r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)', d_content)
    if r:
        headers = {'User-Agent': user_agent, 'Referer': link}
        dl_url = "https:" + r.group(1) + append_headers(headers)
        dl_url2 = dl_url.split('|')[0]
        LOGGER.info(f'dl_url2: {dl_url2}')
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

        

