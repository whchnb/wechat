# -*- coding: utf-8 -*-
"""

@Time    : 20-3-6 下午8:10
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : wechatConfig.py

"""
import time
import hashlib
import requests
from wechat.config import sysConfig
from wechat.database.database import Database


class AccessToken(object):
    access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200
    }

    @classmethod
    def get_access_token(cls, enter=False):
        if enter is True:
            if not cls.access_token.get('access_token') or (time.time() - cls.access_token.get('update_time') > cls.access_token.get('expires_in')):
                url = sysConfig.ACCESSTOKENAPI % (sysConfig.APPID, sysConfig.APPSECRET)
                resp_json = requests.get(url).json()
                print(resp_json)
                if 'errcode' in resp_json:
                    raise Exception(resp_json.get('errmsg'))
                else:
                    db = Database()
                    result = db.inquire('config', {'keyname': 'accessToken'}, ['keyname'])
                    if result is None:
                        db.insert('config', {'keyname': 'accessToken', 'valuename': resp_json.get('access_token')})
                    else:
                        db.update('config', {'keyname': 'accessToken', 'valuename': resp_json.get('access_token')}, ['keyname'])
                    db.close()
                    cls.access_token['access_token'] = resp_json.get('access_token')
                    cls.access_token['expires_in'] = resp_json.get('expires_in')
                    cls.access_token['update_time'] = time.time()
                    return cls.access_token.get('access_token')
            else:
                return cls.access_token.get('access_token')
        else:
            db = Database()
            result = db.inquire('config', {'keyname': 'accessToken'}, ['keyname'])
            db.close()
            cls.access_token['access_token'] = result['valuename']
            return cls.access_token.get('access_token')


class CustomeMd5():
    def md5Generate(self, s):
        m2 = hashlib.md5()
        m2.update(s.encode("utf-8"))
        return m2.hexdigest()[:16].upper()
