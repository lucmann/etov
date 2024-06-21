#!/usr/bin/env python3
# encoding=utf-8


import base64
import json
import logging
import string
import sys
import time
from ocr import Ocr
from session import HttpSession as hs

logger = logging.getLogger(__name__)


class Vote(object):
    def __init__(self):
        self.ocr = Ocr()
        hs.setHost('http://4020140053056.vote.n.weimob.com')
        hs.allowProxy(True)

    def captcha(self, url, body, headers):
        try:
            response = hs.post(url, headers=headers, body=body)
            if response.status_code != 200:
                raise Exception('Failed to request captcha')

            response_body = response.json()
            # logger.info(response_body)

            if int(response_body['errcode']) != 0:
                raise Exception('Failed to get captcha')

            return self.ocr.read_digit_image(base64.b64decode(
                bytes(response_body['data'], 'utf-8')
            ))
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    v = Vote()

    headers = {
        "Host": "4020140053056.vote.n.weimob.com",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "x-tp-signature": "111feaa914b290de0d480635d3e5a16c80c5231a",
        "x-tp-uuid": "112c9a9e9f7d31b55c8cc723e7bc7bb5dbef30fe",
        "Accept": "*/*",
        "Origin": "http://4020140053056.vote.n.weimob.com",
        "Referer": "http://4020140053056.vote.n.weimob.com/saas/vote/4020140053056/25859/app/player/449125",
        "Cookie": "saas.express.session=s%3Ap59vCKDnaDAcG7W1yFXGI9UpE17FPs55.ssJdwn9dO503%2F8JTYqlHQxw6rIBmRQ6rD2JmLQXLQas;",
        # "Cookie": "saas.express.session=s%3ApUSdjTFSdgIPhGuT01om8PTkV2maSAFE.R0pS95TFL4xN6N9R3Y1u434ouUu3VJ%2BHC83lJ5Q49zQ; rprm_cuid_time=1718285699742; rprm_cuid=285699742c164h70tb2o; rprm_uuid=285699742c164h70tb2o; rprm_appShowId2=-lxf959k8fh3dhbhk6eh"
    }

    headers2 = {
        "Host": "4020140053056.vote.n.weimob.com",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "x-tp-signature": "111febab14b290de0d490635d3e5a16c80c5231a",
        "x-tp-uuid": "112c9a9e9e1d31b55c8cc723f6bc7bb5dbef30fe",
        "Accept": "*/*",
        "Origin": "http://4020140053056.vote.n.weimob.com",
        "Referer": "http://4020140053056.vote.n.weimob.com/saas/vote/4020140053056/25859/app/player/449125",
        "Cookie": "saas.express.session=s%3ApUSdjTFSdgIPhGuT01om8PTkV2maSAFE.R0pS95TFL4xN6N9R3Y1u434ouUu3VJ%2BHC83lJ5Q49zQ; rprm_appShowId2=-lxf959k8fh3ahbhk6eh"
    }

    headers3 = {
    }
    reqs = {
        'sess': {
            'url': '/authorize/pub/service/callback/4020140053056/page?code=051CUUFa1VAvEH0xjQFa1L9wlX3CUUFr&state=oauth_state_830da7898eb941179a3dfd984145e36e&appid=wxa3f30fbeb034768f',
        },
        'vote': {
            'url': '/api3/interactive/advance/vote/vote',
            'body': {
                "id": "25859",
                "pid": "4020140053056",
                "player": 449125,
                "storeId": 0,
                "openid": "oIwxACDaaB-i3f98w9nmUywkHLVx",
                "source": 0
            }
        },
        'captcha': {
            'url': '/api3/interactive/advance/vote/captcha/generate',
            'body': {
                "id": "25859",
                "activityid": "25859",
                "pid": "4020140053056",
                "store_id": "0",
                "source": 0
            }
        },
        'checkCaptcha': {
            'url': '/api3/interactive/advance/vote/checkCaptcha',
            'body': {
                "id": "25859",
                "pid": "4020140053056",
                "inputCaptcha": "4qd8",
                "source": 0
            }
        }
    }

    while True:
        captcha_str_list = v.captcha(reqs['captcha']['url'],
                                     reqs['captcha']['body'], headers)

        if len(captcha_str_list) == 1 and len(captcha_str_list[0]) == 4:
            reqs['checkCaptcha']['body']['inputCaptcha'] = "{}".format(captcha_str_list[0])
            res = hs.post(reqs['checkCaptcha']['url'],
                          reqs['checkCaptcha']['body'],
                          headers).json()

            print(res)
            if int(res['errcode']) == 0:
                res = hs.post(reqs['vote']['url'],
                              reqs['vote']['body'], headers).json()
                print(res)
                break

