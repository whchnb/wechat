'''
ngrok.exe http 45480
'''
import sys
import json
import requests

from wechat import templates
#from urllib.parse import urlencode
#from wechat.config import sysConfig
#from wechat.config import contentConfig
#from wechat.chatManage.reply import Reply
#from wechatpy.utils import check_signature
#from wechat.manage.changeMenu import CustomMenu
from flask import Flask, request, redirect, jsonify, render_template
#from wechatpy.exceptions import InvalidSignatureException


app = Flask(__name__)
app.config.from_object(templates)

def getClassData():
    path = '/root/wechat/wechat/static/classes.json'
    if sys.platform == 'win32':
        path = r'D:\wechat\wechat\static\classes.json'
    with open(path, 'r', encoding='utf-8') as f:
        file = f.read()
    classDatas = json.loads(file)
    classMenu = list(classDatas.keys())
    classOneDatas = []
    for className, classData in classDatas.items():
        for cls in classData['classes']:
            if cls['remark'] != '':
                cls['title'] = className
                classOneDatas.append(cls)
                continue
    return classMenu, classOneDatas, classDatas

# 微信公众号登录
@app.route('/', methods=['GET', 'POST'])
def wechatCheckLogin():
    if request.method == 'GET':
        # pass
        signature = request.args.get('signature')
        echostr = request.args.get('echostr')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        try:
            check_signature(token=sysConfig.TOKEN, signature=signature, timestamp=timestamp, nonce=nonce)
            print(echostr)
            return echostr
        except InvalidSignatureException:
            return 'failed'
    else:
        # print(request.form)
        message = Reply(request)
        # message.text(message.Content)
        return message.reply()

@app.route('/', methods=['GET'])
def ok():
    return 'ok'

@app.route('/index', methods=['GET'])
def index():
    return render_template('home-01.html', classMenu=classMenu, classOneDatas=classOneDatas)

@app.route('/more_class', methods=['GET'])
def moreClass():
    classname = request.args.get('classname')
    classData = classDatas[classname]['classes']
    return render_template('courses.html', classDatas=classData)

if __name__ == '__main__':
    #m = CustomMenu('init')
    #m.create(m.default())
    classMenu, classOneDatas, classDatas = getClassData()
    app.run(host='0.0.0.0', port=45480)
    #app.run(host='127.0.0.1', port=45480)
    # print(classMenu)
    # print(classOneDatas)
    # print(classDatas)
    # app.run(host='localhost', port=45480)
