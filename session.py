#!/usr/bin/env python3
# encoding=utf-8

import requests


class HttpSession(object):
    def __init__(self, host, proxies=None):
        self.host = host
        self.sess = requests.Session()
        self.proxies = proxies

        if self.proxies is None:
            self.sess.trust_env = False

    def post(self, url, body=None, headers=None):
        try:
            return self.sess.post(self.host+url, json=body, headers=headers, proxies=self.proxies)
        except Exception as e:
            logger.exception(e)

