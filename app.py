'''
ngrok.exe http 4548
'''
import datetime
from flask import Flask, jsonify, request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply
from reply import Reply


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def wechatCheckLogin():
    if request.method == 'GET':
        signature = request.args.get('signature')
        echostr = request.args.get('echostr')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        try:
            check_signature(token='1573565lwh', signature=signature, timestamp=timestamp, nonce=nonce)
            return echostr
        except InvalidSignatureException:
            return False
    else:
        pass




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4548)