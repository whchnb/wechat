# -*- coding: utf-8 -*-
"""

@Time    : 20-3-7 下午10:52
@Author  : Liwenhao
@Email   : wh.chnb@gmail.com
@File    : send.py

"""
import time
import json
import requests
from wechat.config import sysConfig
from wechat.chatManage.reply import Message
from wechat.manage.tagManager import TagManage


class SendMessage(Message):
    contentData = {
        'learn': '学习%s' % time.time(),
        'couples': '情侣%s' % time.time(),
        'shop': '店铺%s' % time.time(),
    }

    def send(self, tagName):
        tagManage = TagManage()
        print(tagManage.allTag)
        tagId = tagManage.allTag[tagName]['id']
        print(tagId)
        data = {
            "filter": {
                "is_to_all": False,
                "group_id": tagId
            },
            "text": {
                "content": self.contentData[tagName]
            },
            "msgtype": "text"
        }
        url = sysConfig.CONTENTSENDAPI % self.accessToken
        # 需要指定json编码的时候不会对中文转码为unicode，否则群发的消息会显示为unicode码,不能正确显示
        response = requests.post(url=url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))  # 此处的必须指定此参数
        print(response)
        print(response.text)


if __name__ == '__main__':
    sendMessage = SendMessage()
    for i in ['learn', 'couples', 'shop']:

        sendMessage.send(i)