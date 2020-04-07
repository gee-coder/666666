import http.client
import hashlib
import urllib
import random
import json

appid = '20200118000376520'  # 填写你的appid
secretKey = 'DaTrOnbnCcZl6vh4g7Vq'  # 填写你的密钥

myurl = '/api/trans/vip/translate'

fromLang = 'auto'  # 原文语种

httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')


def server(text: str):
    global httpClient
    toLang = 'en'  # 译文语种
    salt = str(random.randint(40000, 65536))
    sign = appid + text + salt + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    httpClient.request('GET', url)
    response = httpClient.getresponse()
    result_all = response.read().decode("utf-8")
    result = json.loads(result_all)
    text = result["trans_result"][0]['dst']
    toLang = 'zh'  # 译文语种
    salt = str(random.randint(40000, 65536))
    sign = appid + text + salt + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        text) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    httpClient.request('GET', url)
    response = httpClient.getresponse()
    result_all = response.read().decode("utf-8")
    result = json.loads(result_all)
    text = result["trans_result"][0]['dst']
    return text


print(server("配送作业活动是以客户发出的订货信息（即订单）作为配送作业的驱动源的。"))

if httpClient:
    httpClient.close()
