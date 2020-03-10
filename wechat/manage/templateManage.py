# -*- coding: utf-8 -*-
"""

@Time    : 20-3-8 下午12:59
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : templateManage.py

"""
import json
import datetime
import requests
from wechat.config import sysConfig
from wechat.config import contentConfig
from wechat.database.database import Database
from wechat.config.wechatConfig import AccessToken


class TemplateManager():
    def __init__(self, openId, templateName):
        self.accessToken = AccessToken().get_access_token()
        self.openId = openId
        self.templateName = templateName
        self.db = Database()

    def getAllTemplate(self):
        url = sysConfig.GETALLTEMPLATEAPI % self.accessToken
        response = requests.get(url)
        print(response)
        print(response.text)

    def getUserData(self, openId):
        sql = "select * from user where openid='%s'" % openId
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        return result

    def getTemplateData(self):
        sql = "select * from templateData where templateName='%s'" % self.templateName
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchone()
        return result

    def sendTemplateContent(self, openId, sendMsg=None):
        myData = self.getUserData(self.openId)
        coupleData = self.getUserData(openId)
        templateData = self.getTemplateData()
        url = sysConfig.SENDMESSAGEWITHTEMPLATEAPI % self.accessToken
        if self.templateName == 'couples':
            data = contentConfig.COUPLESTEMPLATECONTENT % (openId, templateData['templateId'], myData['nickname'], coupleData['nickname'], str(datetime.datetime.now()))
        else:
            data = contentConfig.COUPLESTOSAYMSGTEMPLATECONTENT % (openId, templateData['templateId'], myData['nickname'], sendMsg, str(datetime.datetime.now()))
        data = json.loads(data)
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        print(response)
        print(response.text)
        if response.json()['errcode'] == 0:
            return {'code': True, 'msg': '绑定成功'}
        return {'code': False, 'msg': response.json()['errmsg']}
