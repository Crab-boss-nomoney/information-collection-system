import requests
from urllib.parse import urlencode


# ip138.com查询
def ip_138(ip):  # 只能传IP
    dict = {'ip': ip, 'datatype': 'json'}
    params = urlencode(dict)  # 字典转字符串
    url = 'http://api.ip138.com/query/?' + params
    headers = {"token": "24025d605a0ba3fba43d096e9ec2e559"}
    rb = requests.get(url, headers=headers)
    response = rb.text
    print(response)

import requests
from urllib.parse import urlparse #URL字符串并提取域名部分。

# ip-api.com查询
def ip_api(domain):  # 可传IP或域名
    #先判断是否是IP
    if is_valid_ip(domain):
        return domain
    else:
        parsed_url = urlparse(domain)
        domain = parsed_url.netloc  #将url里切割剩下域名
        domain = remove_after_colon(domain)
        url = "http://ip-api.com/json/"+domain
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'http://www.baidu.com/'
        }
        rb = requests.get(url, headers=headers)
        response = rb.text
        dict_response = eval(response)  # str转为dict
        print(dict_response['query'])
        return dict_response['query']

#判断是否是ip
import re

def is_valid_ip(ip):
    pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if not pattern.match(ip):
        return False
    octets = ip.split('.')
    for octet in octets:
        if int(octet) > 255:
            return False
    return True


#切割后面具有：的端口ip
def remove_after_colon(string):
    index = string.find(':')
    if index != -1:
        string = string.split(':')[0]
    return string

if __name__ == '__main__':
    ip_api("www.baidu.com")




