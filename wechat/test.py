import requests

from wechat.config.wechatConfig import AccessToken

url = 'https://api.weixin.qq.com/cgi-bin/template/api_set_industry'
params = {
    'access_token': AccessToken().get_access_token()
}
data = {
    "industry_id1": "1",
    "industry_id2": "4"
}
response = requests.post(url, params=params, data=data)
print(response)
print(response.text)
