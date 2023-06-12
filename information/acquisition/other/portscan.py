# -*- coding:utf-8 -*-



import socket
import re
import concurrent.futures
import sys
import os
from urllib import parse

sys.path.append(os.getcwd())

THREADNUM = 64  # 线程数




def get_server(port):
    SERVER = {
        'FTP': '21',
        'SSH': '22',
        'Telnet': '23',
        'SMTP': '25',
        'DNS': '53',
        'DHCP': '68',
        'HTTP': '80',
        'TFTP': '69',
        'HTTP': '8080',
        'POP3': '995',
        'POP3': '110',
        'NetBIOS': '139',
        'IMAP': '143',
        'HTTPS': '443',
        'SNMP': '161',
        'LDAP': '489',
        'SMB': '445',
        'SMTPS': '465',
        'Linux R RPE': '512',
        'Linux R RLT': '513',
        'Linux R cmd': '514',
        'Rsync': '1873',
        'IMAPS': '993',
        'Proxy': '1080',
        'JavaRMI': '10990',
        'Oracle EMCTL': '1158',
        'Lotus': '1352',
        'MSSQL': '1433',
        'MSSQL Monitor': '1434',
        'Oracle': '1521',
        'PPTP': '1723',
        'cPanel admin panel/CentOS web panel': '2082',
        'CPanel admin panel/CentOS web panel': '2083',
        'Oracle XDB FTP': '2100',
        'Zookeeper': '2181',
        'DA admin panel': '2222',
        'Docker': '2375',
        'Zebra': '2604',
        'Gitea Web': '3000',
        'Squid Proxy': '3128',
        'MySQL/MariaDB': '3306',
        'Kangle admin panel': '3312',
        'RDP': '3389',
        'SVN': '3690',
        'Rundeck': '4440',
        'GlassFish': '4848',
        'SysBase/DB2': '5000',
        'PostgreSql': '5432',
        'PcAnywhere': '5632',
        'VNC': '5900',
        'TeamViewer': '5938',
        'CouchDB': '5984',
        'varnish': '6082',
        'Redis': '6379',
        'Aria2': '6800',
        'Weblogic': '9001',
        'Kloxo admin panel': '7778',
        'Zabbix': '8069',
        'RouterOS/Winbox': '8291',
        'BT/宝塔面板': '8888',
        'WebSphere': '9090',
        'Elasticsearch': '9300',
        'Virtualmin/Webmin': '10000',
        'Zabbix agent': '10050',
        'Zabbix server': '10051',
        'Memcached': '11211',
        'FileZilla Manager': '14147',
        'MongoDB': '27017',
        'MongoDB': '28017',
        'SAP NetWeaver': '50000',
        'Hadoop': '50070',
        'hdfs':'9000',
    }
    for k, v in SERVER.items():
        if v == port:
            return '{}:{}'.format(k, port)
    return 'Unknown:{}'.format(port)


PORTS = [21, 22, 23, 25, 26, 37, 47, 49, 53, 69, 70, 79, 80, 81, 82, 83, 84, 88, 89, 110, 111, 119, 123, 129, 135,
         137, 139, 143, 161, 175, 179, 195, 311, 389, 443, 444, 445, 465, 500, 502, 503, 512, 513, 514, 515, 520,
         523, 530, 548, 554, 563, 587, 593, 623, 626, 631, 636, 660, 666, 749, 751, 771, 789, 873, 888, 901, 902, 990,
         992, 993, 995, 1000, 1010, 1023, 1024, 1025, 1080, 1088, 1099, 1111, 1177, 1200, 1234, 1311, 1325, 1352,
         1400, 1433, 1434, 1471, 1515, 1521, 1599, 1604, 1723, 1741, 1777, 1883, 1900, 1911, 1920, 1962, 1991,
         2000, 2049, 2067, 2081, 2082, 2083, 2086, 2087, 2121, 2123, 2152, 2181, 2222, 2323, 2332, 2333, 2375,
         2376, 2379, 2404, 2433, 2455, 2480, 2601, 2604, 2628, 3000, 3001, 3128, 3260, 3269, 3283, 3299, 3306,
         3307, 3310, 3311, 3312, 3333, 3386, 3388, 3389, 3460, 3478, 3493, 3541, 3542, 3560, 3661, 3689, 3690,
         3702,
         3749, 3794, 3780, 3784, 3790, 4000, 4022, 4040, 4063, 4064, 4070, 4200, 4343, 4369, 4400, 4440, 4443,
         4444,
         4500, 4550, 4567, 4664, 4730, 4782, 4786, 4800, 4840, 4848, 4899, 4911, 4949, 5000, 5001, 5006, 5007,
         5008,
         5009, 5060, 5094, 5222, 5269, 5353, 5357, 5431, 5432, 5433, 5555, 5560, 5577, 5601, 5631, 5632, 5666,
         5672,
         5683, 5800, 5801, 5858, 5900, 5901, 5938, 5984, 5985, 5986, 6000, 6001, 6014, 6082, 6371, 6372, 6373, 6374,
         6379, 6390, 6664,
         6666, 6667, 6881, 6969, 7000, 7001, 7002, 7071, 7080, 7218, 7474, 7547, 7548, 7549, 7657, 7777, 7779,
         7903,
         7905, 8000, 8001, 8008, 8009, 8010, 8060, 8069, 8080, 8081, 8082, 8083, 8086, 8087, 8088, 8089, 8090,
         8098,
         8099, 8112, 8126, 8139, 8140, 8161, 8181, 8191, 8200, 8291, 8307, 8333, 8334, 8443, 8554, 8649, 8688,
         8800, 8834, 8880, 8883, 8888, 8889, 8899, 9000, 9001, 9002, 9009, 9014, 9042, 9043, 9050, 9051, 9080,
         9081, 9090, 9092, 9100, 9151, 9160, 9191, 9200, 9300, 9306, 9418, 9443, 9595, 9600, 9869, 9903, 9943,
         9944, 9981, 9990, 9998, 9999, 10000, 10001, 10050, 10051, 10243, 10554, 11211, 11300, 12345, 13579, 14147,
         16010, 16992, 16993, 17000, 17778, 18081, 18245, 18505, 20000, 20547, 21025, 21379, 21546, 22022, 22222,
         23023, 23389, 23424, 25105, 25565, 27015, 27016, 27017, 27018, 27019, 28015, 28017, 28561, 30000, 30718,
         32400,
         32764, 32768, 32769, 32770, 32771, 33389, 33890, 33899, 37777, 38190, 40001, 40049, 40650, 41706, 42178,
         43382, 44818, 47808, 48899, 49152, 49153, 50000, 50010, 50011, 50015, 50030, 50050, 50060, 50070, 50100,
         51106, 53413, 54138, 55443, 55553, 55554, 62078, 64738, 65535]

PROBE = {
    'GET / HTTP/1.0\r\n\r\n'
}


class ScanPort():
    def __init__(self, ipaddr):
        '''
        初始化参数
        '''
        self.ipaddr = ipaddr
        self.port = []
        self.out = []
        self.num = 0

    def socket_scan(self, hosts):
        '''
        端口扫描核心代码
        '''
        global PROBE
        socket.setdefaulttimeout(1)
        ip, port = hosts.split(':')
        try:
            if len(self.port) < 25:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建TCP套接字
                # TCP三次握手建立连接
                result = sock.connect_ex((ip, int(port)))   #调用socket，端口开放则返回0，否则返回错误代码，实现全连接扫描。
                if result == 0:                             # 成功建立TCP链接
                    self.port.append(port)                  # 结果集中增加端口
                    for i in PROBE:                         # 通过HTTP1.1刺探
                        sock.sendall(i.encode())            # 发送完整的TCP数据包
                        response = sock.recv(256)           # 接受最大256byte（字节数）
                        sock.close()
                        if response:
                            break
            else:
                self.num = 1
        except (socket.timeout, ConnectionResetError):
            pass
        except:
            pass

    def run(self, ip):
        '''
        多线程扫描
        '''
        hosts = []
        global PORTS, THREADNUM
        for i in PORTS:
            hosts.append('{}:{}'.format(ip, i))
        try:
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=THREADNUM) as executor:
                executor.map(self.socket_scan, hosts)
        except EOFError:
            pass

    def pool(self):
        out = []
        try:
            if (not parse.urlparse(self.ipaddr).path) and (parse.urlparse(self.ipaddr).path != '/'):
                self.ipaddr = self.ipaddr.replace('http://', '').replace('https://', '').rstrip('/')
            else:
                self.ipaddr = self.ipaddr.replace('http://', '').replace('https://', '').rstrip('/')
                self.ipaddr = re.sub('/\w+', '', self.ipaddr)
            if re.search('\d+\.\d+\.\d+\.\d+', self.ipaddr):
                ipaddr = self.ipaddr
            else:
                ipaddr = socket.gethostbyname(self.ipaddr)
            if ':' in ipaddr:
                ipaddr = re.sub(':\d+', '', ipaddr)
            self.run(ipaddr)
        except Exception as e:
            pass
        #识别服务
        for i in self.out:
            _, port = i.split(':')
            out.append(port)
        for i in self.port:
            if i not in out:
                self.out.append(get_server(i))
        if self.num == 0:
            return list(set(self.out))
        else:
            return ['Portspoof:0']




if __name__ == "__main__":
    print(ScanPort('127.0.0.1').pool())



