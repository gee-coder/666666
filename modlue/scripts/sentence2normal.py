import http.client
import hashlib
import urllib
import random
import json

appid = '20200118000376520'  # 填写你的appid
secretKey = 'DaTrOnbnCcZl6vh4g7Vq'  # 填写你的密钥

myurl = '/api/trans/vip/translate'

fromLang = 'auto'  # 原文语种
toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)

httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')


def server(text: str):
    global httpClient
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
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
