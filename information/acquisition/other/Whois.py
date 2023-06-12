import requests
from lxml import etree
import re


def whois(domain):
    #数据请求
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }
    page = requests.get(url='http://whoissoft.com/' + domain, headers=headers).text
    #数据解析
    all = re.search("<!doctype html>(.*?)\*<br />",page, re.S).group(1)
    target = re.search("</h3>(.*?)Domain Name: (.*?)<br />", all, re.S)
    zhuceshang = re.search("Registrar: (.*?)\.", all, re.S)
    iphone = re.search("Registrar Abuse Contact Phone: (.*?)<br />", all, re.S)
    email = re.search("Registrar Abuse Contact Email: (.*?)<a href=\"(.*?)\">(.*?)</a><br />", all, re.S)
    domianserver = re.search("Registrar WHOIS Server: (.*?)<a href=\"(.*?)\">(.*?)</a><br />", all, re.S)
    lasttime = re.search("of whois database: (.*?) &lt;&lt;&lt;<br />", all, re.S)
    UpdatedDate = re.search("Updated Date: (.*?)<br />", all, re.S)
    CreationDate = re.search("Creation Date: (.*?)<br />", all, re.S)
    RegistryDate = re.search("Registry Expiry Date: (.*?)<br />", all, re.S)
    NameServer = re.findall("Name Server: (.*?)<br />", all, re.S)
    print("主域名：" + target.group(2))
    print("注册商：" + zhuceshang.group(1)+".")
    print("联系邮箱：" + email.group(1) + email.group(3))
    print("联系电话：" + iphone.group(1))
    print("更新时间：" + UpdatedDate.group(1))
    print("创建时间：" + CreationDate.group(1))
    print("过期时间：" + RegistryDate.group(1))
    print("域名服务器：" + domianserver.group(1) + domianserver.group(3))
    print("DNS服务器")
    for ns in NameServer:
        if "href" in ns:
            nns = re.search("(.*?)<a href=\"(.*?)\">(.*?)</a>",ns,re.S)
            print(nns.group(1),nns.group(3))
        else:
            print(ns)
    print("whois数据库的上次更新时间: " + lasttime.group(1))




if __name__ == '__main__':
    whois("51cto.com")


