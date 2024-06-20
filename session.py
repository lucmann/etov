#!/usr/bin/env python3
# encoding=utf-8

import bs4
import logging
import re
import requests
from random import choice

logger = logging.getLogger(__name__)

class HttpSession:
    sess = requests.Session()
    host = ''
    allowProxy = False
    proxies = []

    @classmethod
    def setHost(cls, host):
        cls.host = host

    @classmethod
    def allowProxy(cls, allowed, proxies=[]):
        cls.allowProxy = allowed
        cls.proxies = proxies
        cls.sess.trust_env = allowed

        if cls.allowProxy:
            # If users provide no proxies at all, we handle it by ourselves
            if len(cls.proxies) == 0:
                cls.proxies = cls.getProxies()
        else:
            cls.proxies = [{"proxies": "127.0.0.1:7890"}]

    @classmethod
    def setProxies(cls, proxies=None):
        if proxies is None:
            cls.allowProxy = False
            cls.sess.trust_env = False
            cls.proxies = []
        else:
            cls.allowProxy = True
            cls.sess.trust_env = True
            cls.proxies = proxies

    @classmethod
    def get(cls, url, body=None, headers=None):
        try:
            return cls.sess.get(cls.host+url, json=body, headers=headers)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def post(cls, url, body=None, headers=None):
        try:
            return cls.sess.post(cls.host+url, json=body, headers=headers, proxies=choice(cls.proxies))
        except Exception as e:
            logger.exception(e)

    @classmethod
    def getProxies(cls):
        temp_host = cls.host
        cls.host = 'https://free-proxy-list.net'
        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        try:
            response = cls.get('/', headers=headers)
            parsed = bs4.BeautifulSoup(response.text, 'html.parser')
            print(parsed)
            data = parsed.table.find_all('td')
            _ip = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
            _port = re.compile(r'<td>(\d+)</td>')

            _ips = re.findall(_ip, str(data))
            _ports = re.findall(_port, str(data))

            return [{"http": "{}".format(':'.join(_))} for _ in zip(_ips, _ports)]
        except Exception as e:
            logger.exception(e)
            return [{"http": "127.0.0.1:7890"}]
        finally:
            # Restore the host
            cls.host = temp_host

