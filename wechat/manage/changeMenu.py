# from wechat.reply import Menu
import json
import requests
from wechat.config import menuConfig, sysConfig
from wechat.config.wechatConfig import AccessToken


def singleton(cls):
    _instance = {}

    def inner(username):
        if username not in _instance:
            _instance[username] = cls(username)
        return _instance[username]
    return inner


@singleton
class CustomMenu():
    def __init__(self, username):
        self.username = username

    def media(self):
        postJson = menuConfig.MEDIA
        return postJson

    def default(self):
        postJson = menuConfig.DEFAULT
        return postJson

    def create(self, postData):
        data = json.dumps(postData, ensure_ascii=False)
        postUrl = sysConfig.CREATEMENUAPI % AccessToken.get_access_token(enter=True)
        print(postUrl)
        response = requests.post(postUrl, data=data.encode('utf-8'))
        print(response.text)



def change():
    username = '123'
    customeMenu = CustomMenu(username)
    print(id(customeMenu))
    # pData = customeMenu.getMenu()
    # m = Menu()
    # m.create(pData)

# change()