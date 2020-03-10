import json
import requests


url = 'http://woodwang.top/getInfoByType'
data = {
    'distributorId': 7953334,
    'infoType': 1,
    'requestUrl': 'http://woodwang.top/index.html?distributorId=7953334'
}

headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
response = requests.post(url, data=data)
datas = response.json()['groupInfos']
classData = {i['groupName']: i for i in datas}
print(json.dumps(classData, ensure_ascii=False))
# i = 1
# for data in datas:
#     for item in data['classes']:
#         savePath = r'D:\wechat\wechat\static\images\class\{}'.format(item['imgSrc'])
#         html = requests.get('http://woodwang.top/posters/%s' % item['imgSrc'], headers=headers)
#         with open(savePath, 'wb') as file:  # 以byte形式将图片数据写入
#             file.write(html.content)
#             file.flush()
#             print(i)
#             i += 1
