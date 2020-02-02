
import http.client
import hashlib
import urllib
import random
import json

appid = ''  # 填写你的appid
secretKey = ''  # 填写你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'

fromLang = 'auto'  # 原文语种
toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)

sign = appid + q + str(salt) + secretKey
sign = hashlib.md5(sign.encode()).hexdigest()

httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')


def server(text: str):
    global httpClient
    url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    httpClient.request('GET', url)
    response = httpClient.getresponse()
    result_all = response.read().decode("utf-8")
    result = json.loads(result_all)
    return result

if httpClient:
    httpClient.close()
