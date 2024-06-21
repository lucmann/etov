#!/usr/bin/env python3
# encoding=utf-8

import bs4
import logging
import re
import requests
from random import choice
from retry import retry

logger = logging.getLogger(__name__)
DEFAULT_PROXY = {"http": "127.0.0.1:7890"}

class HttpSession:
    sess = requests.Session()
    host = ''
    allowProxy = False
    proxies = []
    this_proxy = None

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

            # A session uses the same proxy at a time
            cls.this_proxy = choice(cls.proxies)
        else:
            cls.proxies = [DEFAULT_PROXY]

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
    @retry(tries=600, delay=1)
    def get(cls, url, body=None, headers=None):
        try:
            return cls.sess.get(cls.host+url, json=body, headers=headers, verify=False)
        except Exception as e:
            logger.exception(e)

    @classmethod
    @retry(tries=600, delay=1)
    def post(cls, url, body=None, headers=None):
        try:
            r = cls.sess.post(cls.host+url, json=body, headers=headers, proxies=cls.this_proxy,
                              timeout=10)
            if r.status_code != 200:
                raise requests.exceptions.RequestException()

            return r
        except requests.exceptions.RequestException:
            # Pick another proxy and try again
            cls.this_proxy = choice(cls.proxies)
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
            data = parsed.table.find_all('td')
            _ip = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
            _port = re.compile(r'<td>(\d+)</td>')

            _ips = re.findall(_ip, str(data))
            _ports = re.findall(_port, str(data))

            _proxies = [':'.join(_) for _ in zip(_ips, _ports)]
            for p in _proxies:
                logger.info(p)

            return [{"http": "{}".format(p), "https": "{}".format(p)} for p in _proxies]

        except Exception as e:
            logger.exception(e)
            return [{"http": "127.0.0.1:7890"}]
        finally:
            # Restore the host
            cls.host = temp_host

