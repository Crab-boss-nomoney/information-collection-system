import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ScanList, dirList, Port, Cmslist
from .other import dirsearchcmd
from django.db.models import Max
import json
# Create your views here.

from .other.dirsearchcmd import dircmd
from .other.ip import ip_api
from .other.portscan import ScanPort
from .other.subdomain import get_subdomain
from .other.whatcms import getwhatcms
from .other.waf import getwaf

def index(request):
    '''首页'''
    # 获取用户名,url
    if request.POST:
        username = request.user.username
        url = request.POST['url']
        scanlist = ScanList(name=username, url=url)
        scanlist.save()  # 将目标url和用户绑定
        sid = ScanList.objects.all().order_by('-id').first()  # 获取存入数据库中的最大值id，用于绑定其他扫描结果
        # 目录扫描
        fileway = 'F:/pythons/information/acquisition/other/reports/' + str(sid.id) + '.json'  # 扫描结果存储的地方
        dirlist = dirList(sid=sid, url=url, fileway=fileway)  # 通过ForeignKey添加sid，绑定扫描列表的id
        dirlist.save()  # 存入目录扫描的数据库中
        dircmd(url, fileway)  # 将url，目录传入目录扫描程序中
        # 端口扫描
        ip = ip_api(url)  # 将url中提取中域名，解析为ip
        presult = ScanPort(ip).pool()  # 将IP给到端口扫描其中进行扫描
        portlist = Port(sid=sid, ip=ip, port=presult)  # 将数据存入数据库中
        portlist.save()  # 保存
        # 指纹识别
        cresult = getwhatcms(url)  # 将url传入指纹识别的方法中
        print(url, cresult)
        cmslist = Cmslist(sid=sid, url=url, cms=cresult)  # 将数据存入数据库中
        cmslist.save()  # 保存

        return redirect("/allscan")

    return render(request, "scan.html")

@login_required
def allscan(request):
    '''扫描列表'''
    username = request.user.username
    obj = ScanList.objects.filter(name=username).order_by('-id')  # 只显示用户自身的扫描记录
    context = {'obj': obj}
    return render(request, "allscan.html", context)

@login_required
def dirresult(request, sid):
    '''目录扫描结果'''
    # 判断是否存在该sid
    if dirList.objects.filter(sid=sid).exists():
        dirobj = dirList.objects.get(sid=sid)
        file = dirobj.fileway  # 获取结果的保存路径
        if os.path.isfile(file):  # 判断文件是否存在
            if os.path.getsize(file) != 0:  # 判断文件是否为空
                with open(file, 'r') as f:  # 将json数据转为字典
                    data = json.load(f)
                    context = {'obj': data["results"], 'sid': sid}
                return render(request, "dirresult.html", context)
    return render(request, "dirresult.html", {'sid': sid})

@login_required
def portresult(request, sid):
    '''端口扫描结果'''
    obj = Port.objects.filter(sid=sid)  # 查询ip的端口信息
    context = {'obj': obj, 'sid': sid}
    return render(request, "portresult.html", context)

@login_required
def cmsresult(request, sid):
    '''指纹识别结果'''
    obj = Cmslist.objects.filter(sid=sid)  # 查询ip的端口信息
    context = {'obj': obj, 'sid': sid}
    return render(request, "cmsresult.html", context)

@login_required
def wafresult(request, sid):
    '''WAF识别'''
    domain = ScanList.objects.get(id=sid).url #在扫描记录中去除url
    result = getwaf(domain)
    contexe = {'obj':result,'sid':sid}
    return render(request,'wafresult.html', contexe)

@login_required
def httpsresult(request, sid):
    '''https证书'''
    headers = {
             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
         }
    domain = ScanList.objects.get(id=sid).url #在扫描记录中去除url
    parsed_url = urlparse(domain)  #将url取出域名，二级域名
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    print(domain)
    try:
        # https://crt.sh/?q=baidu.com
        results = requests.get('https://crt.sh/?q=' + domain, headers=headers, verify=False)
        soup = BeautifulSoup(results.content, 'html.parser')
        wsd = soup.get_text()
        comp = re.compile(
            r'a:link, a:visited {.*? }|a:hover {.*?}|white-space: .*?;|font-family:.*?;|function\s+s|window.location.href\s+=\s+".*?"|return\s+false;| var _sedoq\s+=\s+_sedoq|_sedoq.partnerid\s+=\s+''316085'';| _sedoq.locale\s+=\s+''zh-cn'';|var\s+s\s+=\s+document.createElement|s.type\s+=\s+''text/javascript'';|s.async\s+=\s+true;|s.src\s+=\s+''.*?'';|var\s+f\s+=\s+document.getElementsByTagName|f.parentNode.insertBefore|/.*?/|pre\s+{|word-wrap:\s+break-word;|}|\s*\(str1\){|\s+\+\s+str1;|\s+\|\s+\|\|\s+{;|\s+\|\|\s+{;|_sedoq.partnerid|\s+=|''316085''|\s+'';|\s+enter\s+your\s+partner\s+id|_sedoq.locale\s+=\s+|zh-cn|language\s+locale|\(function\(\)\s+{|\[0\];|s.type|text/javascript|script|s,\s+f|document.getElementById\(.*?\)|.style.marginLeft|=window|\|\||\s+{|;|en-us,|en-uk,|de-de,|es-er-fr,|pt-br,|\s+.innerWidth2|es-|er-|fr|.innerWidth2|er|-,')
        tih = re.sub(comp, '', wsd)
        tih_list = tih.split('\n')
        tih_list = tih_list[46:-12]
        res1_list = []
        number = 0
        for i in tih_list:
            if i != "":
                res1_list.append(i)
        step = 7
        res2_list = [res1_list[i:i + step] for i in range(0, len(res1_list), step)]
        for i in res2_list:
            number += 1
        number_list = list(range(1, number + 1))
        dict_res = dict(zip(number_list, res2_list))
        contexe = {'status': "yes", 'url': domain, 'res_list': dict_res,'sid':sid}
        return render(request, 'httpsresult.html', contexe)
    except Exception as e:
        contexe =  {'status': "no", 'url': domain,'sid':sid}
        return render(request, 'httpsresult.html', contexe)

@login_required
def subresult(request, sid):
    '''子域名扫描'''
    domain = ScanList.objects.get(id=sid).url #在扫描记录中去除url
    parsed_url = urlparse(domain)  #将url取出域名，二级域名
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    result = get_subdomain(domain)
    contexe = {'obj':result,'sid':sid}
    print(result)
    return render(request,'subresult.html', contexe)



