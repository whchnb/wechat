# -*- coding: utf-8 -*-
"""

@Time    : 20-3-7 下午8:38
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : tagManager.py

"""
import time
import json
import requests
from wechat.config import sysConfig
from wechat.database.database import Database
from wechat.config.wechatConfig import AccessToken


class TagManage():
    def __init__(self):
        self.accessToken = AccessToken.get_access_token()
        self.allTag = self.getAllTag()
        self.db = Database()

    # 获取所有标签
    def getAllTag(self):
        url = sysConfig.ALLTAGAPI % self.accessToken
        response = requests.get(url)
        tagDict = {i['name']: i for i in response.json()['tags']}
        return tagDict

    # 标签添加
    def addTag(self, tagName):
        if tagName not in self.allTag.keys():
            url = sysConfig.ADDTAGAPI % self.accessToken
            data = {
                "tag": {
                    "name": tagName
                }
            }
            response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
            # print(response)
            # print(response.text)
            if 'errcode' in response.text:
                msg = {
                    'code': False,
                    'msg': response.text
                }
            else:
                msg = {
                    'code': True,
                    'msg': '分组创建成功',
                    'data': json.dumps(response.json()['tag'])
                }
        else:
            msg = {
                'code': False,
                'msg': '该分组已存在'
            }
        print(msg)
        self.allTag = self.getAllTag()
        return msg

    # 删除分组
    def deleteTag(self, tagName):
        tagid = self.allTag[tagName]['id']
        url = sysConfig.DELETETAGAPI % self.accessToken
        data = {
            "tag": {
                "id": tagid
            }
        }
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        if response.json()['errcode'] != 0:
            msg = {
                'code': False,
                'msg': response.text
            }
        else:
            msg = {
                'code': True,
                'msg': '分组删除成功'
            }
        print(msg)
        return msg

    # 标签检测
    def checkTag(self, tagName):
        return False if tagName not in self.allTag.keys() else True

    # 获取标签下所有用户
    def getAllUserTag(self, tagName, openId=''):
        tagid = self.allTag[tagName]['id']
        url = sysConfig.USERTAGAPI % self.accessToken
        data = {
            "tagid": tagid,
            "next_openid": openId  # 第一个拉取的OPENID，不填默认从头开始拉取
        }
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return response.json()

    # 为用户添加标签
    def addTagToUser(self, openId, tagName):
        tagid = self.allTag[tagName]['id']
        url = sysConfig.ADDTAGTOUSERAPI % self.accessToken
        data = {
            "openid_list": [openId],
            "tagid": tagid
        }
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        # print(response)
        # print(response.text)
        if response.json()['errcode'] != 0:
            msg = {
                'code': False,
                'msg': response.text
            }
        else:
            msg = {
                'code': True,
                'msg': '用户添加标签成功'
            }
        print(msg)
        return msg

    # 取消用户标签
    def deleteTagFromUser(self, openId, tagName=None, tagId=None):
        tagid = self.allTag[tagName]['id'] if tagId is None else tagId
        url = sysConfig.DELETETAGTOUSERAPI % self.accessToken
        data = {
            "openid_list": [openId],
            "tagid": tagid
        }
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        # print(response)
        # print(response.text)
        if response.json()['errcode'] != 0:
            msg = {
                'code': False,
                'msg': response.text
            }
        else:
            msg = {
                'code': True,
                'msg': '用户标签取消成功'
            }
        print(msg)
        return msg

    # 获取用户标签
    def getUserTag(self, openId):
        url = sysConfig.GETUSERTAGAPI % self.accessToken
        data = {"openid": openId}
        response = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return response.json()


if __name__ == '__main__':
    openId = 'oKGLxw8S9n9ZnKe3v9_u0H8m8k1Q'
    tagManage = TagManage()
    # tagManage.addTag('学习')
    tagManage.deleteTag('learn')
    print(tagManage.allTag)
    # tagManage.addTagToUser(openId, '学习')
    # print(tagManage.getAllUserTag('学习'))
    # print(tagManage.getUserTag(openId))
