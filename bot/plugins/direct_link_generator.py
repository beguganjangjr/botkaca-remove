import json
import time
import re
import aiohttp
import math, json
import urllib.parse
import logging
import lk21
import string
import random
from bs4 import BeautifulSoup
from bot.plugins.exceptions import DirectDownloadLinkException
from bot.plugins import jsunpack
from getuseragent import UserAgent
from bot import CONFIG
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
ua = UserAgent()
ua = ua.Random()
LOGGER = logging.getLogger(__name__)



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

async def direct_link_generator(url, session):
    #blocklinks
    if 'mega.nz' in url or 'drive.google.com' in url or 'uptobox.com' in url \
    or '1fiecher.com' in url or 'googleusercontent.com' in url:
        return "**ERROR:** Unsupported URL!"
    
    #mediafire.com
    elif 'mediafire.com' in url:
        try:
            link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()

            page = BeautifulSoup(restext, 'lxml')
            info = page.find('a', {'aria-label': 'Download file'})
            ourl = info.get('href')
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your mediafire link!"
          
    #disk.yandex.com    
    elif 'yadi.sk' in url or 'disk.yandex.com' in url:
        try:
            link = re.findall(r'\b(https?://.*(yadi|disk)\.(sk|yandex)*(|com)\S+)', url)[0][0]
            print(link)
        except IndexError:
            return "**ERROR:** Cant't download, double check your yadisk link!"

        api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
        try:
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(api.format(link))
                restext = await resp.json()
                ourl = restext['href']
                return ourl
        except:
            LOGGER.exception("Ayee jooo")
            return "**ERROR:** Cant't download, the yadisk file not found or dowmload limit reached!" 

    #zippyshare.com
    elif 'zippyshare.com' in url:
        try:
            link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()
            base_url = re.search('http.+.com', restext).group()
            page_soup = BeautifulSoup(restext, 'lxml')
            scripts = page_soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                                        script.text).group('url')
                    math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                       script.text).group('math')
                    url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            ourl = base_url + eval(url)
            name = urllib.parse.unquote(url.split('/')[-1])
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your zippyshare link!"
       
    #racaty.net
    elif 'racaty.net' in url:
        try:
            link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()                      
            bss=BeautifulSoup(restext,'html.parser')
            op=bss.find('input',{'name':'op'})['value']
            id=bss.find('input',{'name':'id'})['value']
                  
            async with aiohttp.ClientSession() as ttksess:
                rep = await ttksess.post(link,data={'op':op,'id':id})
                reptext = await rep.text()
            bss2=BeautifulSoup(reptext,'html.parser')
            ourl = bss2.find('a',{'id':'uniqueExpirylink'})['href']
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your racaty link!"
       
    elif 'pixeldrain.com' in url:
        url = url.strip("/ ")
        file_id = url.split("/")[-1]
        
        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"

        async with aiohttp.ClientSession() as ttksess:
            resp = await ttksess.get(info_link)
            restext = await resp.json()

        if restext["success"]:
            return dl_link
        else:
            return "**ERROR:** Cant't download, {}.".format(restext["value"])
          
    elif 'mixdrop.co' in url or 'mixdrop.sx' in url:
      web_url = re.findall(r'(?://|\.)(mixdrop\.(?:co|to|sx))/(?:f|e)/(\w+)', url)[0]
      media_id = web_url[1]
      host = web_url[0]
      link = 'https://' + host + '/e/' + media_id
      user_agent = ua
      headers = {'Origin': 'https://{}'.format(host),
                 'Referer': 'https://{}/'.format(host),
                 'User-Agent': user_agent}
      async with session as ses:
        async with ses.get(url=link, headers=headers) as response:
            d_content = await response.text()

            
      #LOGGER.info(f'd_content: {d_content}')  
      r = re.search(r'location\s*=\s*"([^"]+)', d_content)
      if r:
        url = 'https://{0}{1}'.format(host, r.group(1))
        async with session.get(link, headers=headers) as response:
          d_content = await response.text()
      if '(p,a,c,k,e,d)' in d_content:
        d_content = get_packed_data(d_content)
      r = re.search(r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)', d_content)
      if r:
        headers = {'User-Agent': user_agent, 'Referer': link}
        dl_url = "https:" + r.group(1) + append_headers(headers)
        return dl_url
      raise DirectDownloadLinkException("`Error: Can't extract the link`\n")        
      
    elif 'streamtape.com' in url:
        try:
            web_url = re.findall(r'\bhttps?://.*streamtape\.com\S+', url)[0]
            media_id = web_url[1]
            host = web_url[0]
            user_agent = ua
            link = 'https://' + host + '/v/' + media_id
            headers = {'User-Agent': user_agent,
                       'Referer': 'https://{0}/'.format(host)}
            async with session as ses:
                async with ses.get(url=link, headers=headers) as response:
                    d_content = await response.text()
            src = re.search(r'''ById\('vi.+?=\s*["']([^"']+)['"].+?["']([^"']+)''', d_content)
            if src:
                src_url = 'https:{0}{1}&stream=1'.format(src.group(1), src.group(2))
                dl_url = get_redirect_url(src_url, headers) + append_headers(headers)
                return dl_url
        except IndexError:
            raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
                
    elif 'dood.la' in url or 'dood.so' in url or 'dood.cx' in url or 'dood.to' in url:
        web_url = re.findall(r'(?://|\.)(dood(?:stream)?\.(?:com|watch|to|so|cx|la))/(?:d|e)/([0-9a-zA-Z]+)', url)[0]
        media_id = web_url[1]
        host = web_url[0]
        link = 'https://' + host + '/e/' + media_id
        user_agent = ua
        headers = {'User-Agent': user_agent,
                   'Referer': 'https://{0}/'.format(host)}
        link.replace('/d/','/e/')
        proxies = 'http://{0}'.format(CONFIG.PROXY)
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url=link, headers=headers, proxy=proxies) as response:
                text = await response.text()
           
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
            LOGGER.info(f'dl_url: {dl_url}')
            return dl_url
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
                    
            
            
        
        
        
            
    
      
          
