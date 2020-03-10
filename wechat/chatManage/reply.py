# encoding: utf-8
"""
@author: Liwenhao
@e-mail: wh.chnb@gmail.com
@file: reply.py
@time: 2020/2/9 17:34
@desc:
"""
import json
import time
import requests
from lxml import etree
from flask import make_response
from wechat.yiban import dataInfo
from wechat.config import sysConfig
from wechat.config import contentConfig
from wechat.database.database import Database
from wechat.manage.tagManager import TagManage
from wechat.config.wechatConfig import AccessToken
from wechat.manage.userManage import CouplesManage
from wechat.manage.templateManage import TemplateManager


class Message(object):
    def __init__(self, req=None):
        self.request = req
        self.token = sysConfig.TOKEN
        self.AppID = sysConfig.APPID
        self.AppSecret = sysConfig.APPSECRET
        self.accessToken = AccessToken.get_access_token()


class Post(Message):
    def __init__(self, req):
        super(Post, self).__init__(req)
        self.xml = etree.fromstring(req.stream.read())
        self.messageList = [i.tag for i in self.xml.getiterator()]
        print(self.messageList)
        self.MsgType = self.xml.find("MsgType").text
        self.ToUserName = self.xml.find("ToUserName").text
        self.FromUserName = self.xml.find("FromUserName").text
        self.CreateTime = self.xml.find("CreateTime").text
        print('消息由%s 发送给 %s:' % (self.FromUserName, self.ToUserName))
        print('MsgType 类型:', self.MsgType)
        if self.MsgType == 'event' and 'Status' not in self.messageList:
            self.EventKey = self.xml.find('EventKey').text
            self.Event = self.xml.find("Event").text
        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
            'event': ['EventKey'],
        }
        attributes = hash_table[self.MsgType]
        self.Content = self.xml.find("Content").text if 'Content' in attributes else '抱歉，暂未支持此消息。'
        self.PicUrl = self.xml.find("PicUrl").text if 'PicUrl' in attributes else '抱歉，暂未支持此消息。'
        self.MediaId = self.xml.find("MediaId").text if 'MediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Format = self.xml.find("Format").text if 'Format' in attributes else '抱歉，暂未支持此消息。'
        self.ThumbMediaId = self.xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Location_X = self.xml.find("Location_X").text if 'Location_X' in attributes else '抱歉，暂未支持此消息。'
        self.Location_Y = self.xml.find("Location_Y").text if 'Location_Y' in attributes else '抱歉，暂未支持此消息。'
        self.Scale = self.xml.find("Scale").text if 'Scale' in attributes else '抱歉，暂未支持此消息。'
        self.Label = self.xml.find("Label").text if 'Label' in attributes else '抱歉，暂未支持此消息。'
        self.Title = self.xml.find("Title").text if 'Title' in attributes else '抱歉，暂未支持此消息。'
        self.Description = self.xml.find("Description").text if 'Description' in attributes else '抱歉，暂未支持此消息。'
        self.Url = self.xml.find("Url").text if 'Url' in attributes else '抱歉，暂未支持此消息。'
        self.Recognition = self.xml.find("Recognition").text if 'Recognition' in attributes else '抱歉，暂未支持此消息。'
        # self.Event = self.xml.find("Event").text if 'Event' in attributes else '抱歉，暂未支持此消息。'


class Reply(Post):
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.db = Database()
        # self.checkUser()
        self.xml = contentConfig.BASECONTENT.format(self.FromUserName, self.ToUserName, str(int(time.time())))
        self.check()
        self.db.close()

    # 检测用户是否存在， 不存在插入， 存在更新最后登录时间
    def checkUser(self):
        url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        params = {
            'access_token': AccessToken.get_access_token(),
            'openid': self.FromUserName,
            'lang': 'zh_CN'
        }
        response = requests.get(url, params=params)
        # print(response)
        # print(response.text)
        data = response.json()
        nickName = data['nickname']
        sex = data['sex']
        province = data['province']
        groupid = data['groupid']
        remark = data['remark']
        subscribe_time = data['subscribe_time']
        subscribe_scene = data['subscribe_scene']
        qr_scene = data['qr_scene']
        qr_scene_str = data['qr_scene_str']
        headimgurl = data['headimgurl']
        userData = {
            'nickname': nickName,
            'sex': sex,
            'province': province,
            'groupid': groupid,
            'remark': remark,
            'subscribeTime':  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(subscribe_time)),
            'subscribeScene':  subscribe_scene,
            'qrScene': qr_scene,
            'qrSceneStr': qr_scene_str,
            'headimgurl': headimgurl
        }
        return userData

    # 自定义图文消息
    def customePictureContent(self, datas):
        length = len(datas)
        self.xml = contentConfig.ARTICLECONTENT.format(self.FromUserName, self.ToUserName, str(int(time.time())), length)
        contentList = []
        for data in datas:
            content = contentConfig.PICTURECONTENT.format(data['title'], data['content'], data['imageUrl'], data['url'])
            contentList.append(content)
        self.testarea = ' '.join(contentList)

    # 检测
    def check(self):
        userData = self.checkUser()
        userData['openid'] = self.FromUserName
        result = self.db.inquire('user', userData, ['openid'])
        if result is not None:
            self.db.update('user', userData, ['openid'])
        msg = '抱歉，暂未支持此消息'
        tagManage = TagManage()
        self.testarea = contentConfig.MSGCONTENT.format('我的分组 %s' % tagManage.getUserTag(self.FromUserName))
        if self.MsgType == 'event' and 'Status' not in self.messageList:
            print(self.EventKey)
            print(self.Event)
            if self.Event == 'subscribe':
                if result is None:
                    self.testarea = contentConfig.MSGCONTENT.format('感谢您的关注')
                    self.db.insert('user', userData)
                else:
                    if result['isFollow'] == 0:
                        userData['isFollow'] = 1
                        self.db.update('user', userData, ['openid'])
                        self.testarea = contentConfig.MSGCONTENT.format('取关了还关注？')
            if self.Event == 'unsubscribe':
                userData = {}
                userData['openid'] = self.FromUserName
                userData['isFollow'] = 0
                self.db.update('user', userData, ['openid'])
                pass
            if self.EventKey == 'V1001_TODAY_MUSIC':
                # self.testarea = contentConfig.MSGCONTENT
                datas = [
                    {'title': '今日歌曲', 'content': '今日歌曲', 'imageUrl': 'https://qpic.y.qq.com/music_cover/JBDCVgqXWXaYUvcsElqcicY1Jk0VwBsfS9iaJC9zVlWAzvvDZqjjslNQ/600?n=1', 'url': 'https://y.qq.com/n/yqq/playlist/7449996326.html#stat=y_new.index.playlist.pic'},
                    {'title': '今日歌曲', 'content': '今日歌曲', 'imageUrl': 'https://qpic.y.qq.com/music_cover/JBDCVgqXWXaYUvcsElqcicY1Jk0VwBsfS9iaJC9zVlWAzvvDZqjjslNQ/600?n=1', 'url': 'https://y.qq.com/n/yqq/playlist/7449996326.html#stat=y_new.index.playlist.pic'},
                    {'title': '今日歌曲', 'content': '今日歌曲', 'imageUrl': 'https://qpic.y.qq.com/music_cover/JBDCVgqXWXaYUvcsElqcicY1Jk0VwBsfS9iaJC9zVlWAzvvDZqjjslNQ/600?n=1', 'url': 'https://y.qq.com/n/yqq/playlist/7449996326.html#stat=y_new.index.playlist.pic'},
                ]
                self.customePictureContent(datas)
            if self.EventKey == 'V1001_LEARN_YIBAN':
                # self.testarea = contentConfig.MSGCONTENT
                datas = dataInfo.yiban()
                self.customePictureContent(datas)
            if self.EventKey == 'V1001_CHANGE_GROUP_1':
                self.testarea = contentConfig.MSGCONTENT.format('正在设置')
                # m = CustomMenu(self.FromUserName)
                # m.create(m.media())
            if self.EventKey in sysConfig.TAGDATA.keys():
                tagName = sysConfig.TAGDATA[self.EventKey]
                tagStatus = tagManage.checkTag(tagName)
                if tagStatus is False:
                    tagManage.addTag(tagName)
                    # tagStatus = tagManage.checkTag(tagName)
                # if tagStatus is True:
                #     tagManage.addTag(tagName)
                tagIdList = tagManage.getUserTag(self.FromUserName)['tagid_list']
                if len(tagIdList) != 0:
                    tagId = tagIdList[0]
                    msg = tagManage.deleteTagFromUser(self.FromUserName, tagId=tagId)
                msgData = tagManage.addTagToUser(self.FromUserName, tagName)
                if msgData['code'] is True:
                    # 从数据库查询用户信息
                    msg = '您已被移至%s分组' % tagName
                    if self.EventKey == 'V1001_TAG_COUPLES':
                        couplesManage = CouplesManage(self.FromUserName)
                        couplesBindStatus = couplesManage.checkBind()
                        if couplesBindStatus['code'] is False:
                            msg = '当前未与TA绑定关系\n\n绑定方法:\n    step1:后台回复“情侣绑定”获取密钥\n    step2: 好友关注公众号\n    step3:请让TA选择情侣分组\n    step4:将密钥发送到本公众号\n(每人仅可完成一次绑定)'
                        else:
                            otherCouplesData = couplesManage.getUserData(couplesBindStatus['couplesOpenId'])
                            msg = '请将想要对%s说的话告诉我' % otherCouplesData['nickname']
                            userData  = {'openid': self.FromUserName, 'operation': 'SEND_TO_COUPLES'}
                            self.db.update('user', userData, ['openid'])
                        couplesManage.db.close()
                self.testarea = contentConfig.MSGCONTENT.format(msg)
        if self.MsgType == 'text':
            couplesManage = CouplesManage(self.FromUserName)
            if self.Content == '1':
            # if self.Content == '情侣绑定':
                couplesBindStatus = couplesManage.checkBind()
                msg = 'couples_' + couplesBindStatus['couplesMd5']
            if self.Content.startswith('couples_'):
                couplesMd5 = self.Content.split('couples_')[1]
                couplesBindStatus = couplesManage.couplesBind(couplesMd5)
                if couplesBindStatus['code'] is True:
                    msg = couplesBindStatus['msg']
                else:
                    msg = couplesBindStatus['msg']
            else:
                operation = self.db.inquire('user', userData, ['openid'])
                if operation['operation'] == 'SEND_TO_COUPLES':
                    couplesBindStatus = couplesManage.checkBind()
                    otherCouplesData = couplesManage.getUserData(couplesBindStatus['couplesOpenId'])
                    templateManager = TemplateManager(self.FromUserName, 'couplesMsg')
                    status = templateManager.sendTemplateContent(couplesBindStatus['couplesOpenId'], sendMsg=self.Content)
                    templateManager.db.close()
                    if status['code'] is True:
                        data = {'openid': self.FromUserName, 'operation': ''}
                        self.db.update('user', data=data, param=['openid'])
                        msg = '消息已发送至: %s' % otherCouplesData['nickname']
                    else:
                        msg = '消息发送失败'
            couplesManage.db.close()
            self.testarea = contentConfig.MSGCONTENT.format(msg)

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self, ThumbMediaId, Title='', Description='', MusicURL='', HQMusicUrl=''):
        pass

    def reply(self):
        content = self.xml % self.testarea
        # print(content)
        response = make_response(content)
        response.content_type = 'application/xml'
        return response


