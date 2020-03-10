import re
import requests
from urllib.parse import urljoin

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'ajaxFunction': 'true',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '108',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'woodwang.top',
    'Origin': 'http://woodwang.top',
    'Pragma': 'no-cache',
    'Referer': 'http://woodwang.top/index.html?distributorId=7953334',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def getYibanUrl(fromId):
    url = 'http://woodwang.top/js/my.js'
    response = requests.get(url, headers=headers)
    yibanUrl = re.findall(re.compile(r"var yiBanUrl\s*?=\s*?'(.*?)'", re.S), response.text)[0]
    indexImage = re.findall(re.compile(r'<img src="(.*?)"', re.S), response.text)[0]
    indexImageUrl = urljoin('http://woodwang.top', indexImage)
    data = {
        'url': yibanUrl + fromId,
        'imageUrl': indexImageUrl,
        'title': '【益伴推广大使】召集令',
        'content': '【益伴推广大使】召集令'
    }
    return data


def getFormId(requestUrl, distributorId):
    url = 'http://woodwang.top/getInfoByType'
    data = {
        'distributorId': distributorId,
        'infoType': '1',
        'requestUrl': requestUrl
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['authInfo']['fromId']


def shop(requestsUrl):
    distributorId = '7953334'
    fromId = getFormId(requestsUrl, distributorId)
    data = getYibanUrl(fromId)
    return data


def yiban():
    requestsList = [
        {'title': '轻课商城', 'url': 'http://woodwang.top/index.html?distributorId=7953334'},
        {'title': '轻课精选', 'url': 'http://woodwang.top/bonus.html?distributorId=7953334'},
        {'title': '轻课商城-功能分类版', 'url': 'http://woodwang.top/all.html?distributorId=7953334'},
        {'title': '轻课商城-英语专场', 'url': 'http://woodwang.top/english.html?distributorId=7953334'},
        {'title': '轻课商城-小分类专场', 'url': 'http://woodwang.top/other.html?distributorId=7953334'},
    ]
    dataList = []
    for requestsData in requestsList:
        data = shop(requestsData['url'])
        data['url'] = requestsData['url']
        data['title'] = requestsData['title']
        dataList.append(data)
    return dataList
