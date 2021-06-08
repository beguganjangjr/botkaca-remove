import logging
import json
import math
import re
import urllib.parse
from os import popen
from random import choice
from urllib.parse import urlparse

import lk21
import requests
from bs4 import BeautifulSoup
from js2py import EvalJs
from lk21.extractors.bypasser import Bypass
from base64 import standard_b64encode
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

async def generate_directs(url):
  if 'zippyshare.com' in url:
    try:
      link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
      restext = (requests.get(url)).text
      base_url = re.search('http.+.com', response_text).group()
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
      dl_url = base_url + eval(url)
      name = urllib.parse.unquote(url.split('/')[-1])
      return dl_url
    
    except KeyError:
      raise DirectDownloadLinkException("**ERROR:** Cant't download, double check your zippyshare link!")
  
  
  elif 'racaty.net' in url:
    dl_url = ''
    try:
      link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
      reqs=requests.get(url)
      bss=BeautifulSoup(reqs.text,'html.parser')
      op=bss.find('input',{'name':'op'})['value']
      id=bss.find('input',{'name':'id'})['value']
      rep=requests.post(link,data={'op':op,'id':id})
      bss2=BeautifulSoup(rep.text,'html.parser')
      dl_url=bss2.find('a',{'id':'uniqueExpirylink'})['href']
      return dl_url
    except IndexError:
      raise DirectDownloadLinkException("`No Racaty links found`\n")
      
  elif 'pixeldrain.com' in url:
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
    dl_link = f"https://pixeldrain.com/api/file/{file_id}"
    resp = request.get(info_link)
    restext = resp.json()
    if restext["success"]:
      return dl_link
    else:
      return "**ERROR:** Cant't download, {}.".format(restext["value"])
      
  elif 'mediafire.com' in url:
    try:
      link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
      page = BeautifulSoup(requests.get(link).content, 'lxml')
      info = page.find('a', {'aria-label': 'Download file'})
      dl_url = info.get('href')
      return dl_url
    except IndexError:
      raise DirectDownloadLinkException("`No MediaFire links found`\n")
      
  elif 'hxfile.co' in url:
    
    dl_url = ''
    try:
      link = re.findall(r'\bhttps?://.*hxfile\.co\S+', url)[0]
      #bypasser = lk21.Bypass()
      dl_url= Bypass.bypass_url(link)
      return dl_url
    except IndexError:
       raise DirectDownloadLinkException("`No Hxfile links found`\n")
      
      
      
