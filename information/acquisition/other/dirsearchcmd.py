import os
import re
import socket


def dircmd(url,file):
    try:
        with open(file, "w") as fd:
            c = 'python F:/pythons/information/acquisition/dirsearch/dirsearch.py -u ' + url + ' --format json -o ' + file
            print(c)
            os.system(c)
    except:
        pass



import requests
from bs4 import BeautifulSoup

def test(domain):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
    r = requests.get('http://whoissoft.com/' + domain, headers=headers)
    csd = r.content.decode('utf-8')
    soup = BeautifulSoup(csd, 'html.parser')
    print(soup.text)


def socket_scan(self, hosts):
    '''端口扫描核心代码'''
    global PROBE
    socket.setdefaulttimeout(1)
    ip, port = hosts.split(':')
    try:
        if len(self.port) < 25:
            # 创建套接字
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # TCP/IP三次握手建立连接
            result = sock.connect_ex((ip, int(port)))
# 调用socket.connect_ex((ip, port))，端口开放返回0，否则返回错误代码
# 实现和nmap的全连接扫描类似的功能。
            if result == 0:                     # 成功建立TCP链接
                self.port.append(port)          # 结果集中增加端口
                for i in PROBE:                 # 通过HTTP1.1刺探
                    sock.sendall(i.encode())    # 发送完整的TCP数据包
                    response = sock.recv(256)   # 接受最大256byte
                    sock.close()
                    if response:
                        break
                if response:
                    for pattern in SIGNS:
                        pattern = pattern.split(b'|')
                        if re.search(pattern[-1],response, re.IGNORECASE):
# 正则匹配banner信息与字典中的服务
                            proto = '{}:{}'.format(pattern[1].decode(), port)
                            self.out.append(proto)  # 添加至输出结果
                            break
        else:
            self.num = 1
    except (socket.timeout, ConnectionResetError): # 异常处理
        pass
    except:
        pass


if __name__ == '__main__':
    test("jd.com")