#!/usr/bin/env python3
# encoding=utf-8

import requests


class HttpSession:
    sess = requests.Session()
    host = ''
    allowProxy = False
    proxies = None

        # if self.proxies is None:
            # self.sess.trust_env = False

    @classmethod
    def setHost(cls, host):
        cls.host = host

    @classmethod
    def setProxies(cls, proxies=None):
        if proxies is None:
            cls.allowProxy = False
            cls.sess.trust_env = False
        else:
            cls.allowProxy = True
            cls.sess.trust_env = True

        cls.proxies = proxies

    @classmethod
    def post(cls, url, body=None, headers=None):
        try:
            return cls.sess.post(cls.host+url, json=body, headers=headers, proxies=cls.proxies)
        except Exception as e:
            logger.exception(e)

