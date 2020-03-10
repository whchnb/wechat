# -*- coding: utf-8 -*-
"""

@Time    : 20-3-6 下午10:00
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : userInfo.py

"""
import time
from wechat.config import sysConfig
from wechat.database.database import Database
from wechat.manage.templateManage import TemplateManager
from wechat.config.wechatConfig import AccessToken, CustomeMd5





class UserManage():
    def __init__(self, openId):
        self.openId = openId
        self.db = Database()
        pass

    def addTag(self, tagName):
        url = sysConfig.ADDTAGAPI % AccessToken.get_access_token()
        data = {
            "tag": {
                "name": tagName
            }
        }
        pass


class CouplesManage(UserManage):
    def __init__(self, openId):
        super(CouplesManage, self).__init__(openId)
        self.couplesMd5 = self.getCouples()

    def checkCouplesMd5(self, couplesMd5):
        sql = "select count(*) counts from couples where couplesMd5='%s'" % couplesMd5
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        if result['counts'] == 0:
            return {'code': False, 'msg': '密钥不存在，请检查密钥真实性'}
        elif result['counts'] == 2:
            return {'code': False, 'msg': '此密钥已被绑定'}
        else:
            return {'code': True, 'couplesMd5': couplesMd5}

    def checkCouples(self):
        sql = "select * from couples where openId='%s'" % self.openId
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        if result is None:
            return {'code': False}
        return {'code': True, 'openId': self.openId, 'couplesMd5': result['couplesMd5']}

    def getCouples(self):
        status = self.checkCouples()
        if status['code'] is False:
            s = 'couples_%s_%s' % (self.openId, time.time())
            print(s)
            couplesMd5 = CustomeMd5().md5Generate(s)
            data = {'openId': self.openId, 'couplesMd5': couplesMd5}
            self.db.insert('couples', data)
            status = self.checkCouples()
        return status['couplesMd5']

    def getMd5HosterOpenId(self, couplesMd5):
        sql = "select * from couples where couplesMd5='%s'" % couplesMd5
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        return result

    def checkBind(self):
        sql = "select * from couples where couplesMd5='%s' and openId != '%s'" % (self.couplesMd5, self.openId)
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        if result is None:
            return {'code': False, 'couplesMd5': self.couplesMd5}
        return {'code': True, 'couplesOpenId': result['openId'], 'couplesMd5': self.couplesMd5}

    def getUserData(self, openId):
        sql = "select * from user where openid='%s'" % openId
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        return result

    def couplesBind(self, couplesMd5):
        status = self.checkCouplesMd5(couplesMd5)
        if status['code'] == True:
            otherUserData = self.getMd5HosterOpenId(couplesMd5)
            # 绑定成功， 调用模板发送消息
            templateManager = TemplateManager(self.openId, 'couples')
            status = templateManager.sendTemplateContent(otherUserData['openId'])
            templateManager.db.close()
            if status['code'] is True:
                data = {'openId': self.openId, 'couplesMd5': couplesMd5}
                self.db.update('couples', data=data, param=['openId'])
                return {'code': True, 'msg': '绑定成功'}
            return status
        else:
            return status