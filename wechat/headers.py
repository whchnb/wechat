old_headers = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
ajaxFunction: true
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 108
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Host: woodwang.top
Origin: http://woodwang.top
Pragma: no-cache
Referer: http://woodwang.top/index.html?distributorId=7953334
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
X-Requested-With: XMLHttpRequest"""
headers = old_headers.split('\n')
for i in headers:
    print("'{}': '{}',".format(i.split(': ')[0].strip(), i.split(': ')[1].strip()))
