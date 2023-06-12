import re

import requests
from bs4 import BeautifulSoup


def gethttps(domain):

    headers = {
             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
         }
    try:
        # https://crt.sh/?q=baidu.com
        results = requests.get('https://crt.sh/?q=' + domain, headers=headers,verify=False)
        #print(results.text)
        soup = BeautifulSoup(results.content, 'html.parser')

        wsd = soup.get_text()
        comp = re.compile(
            r'a:link, a:visited {.*? }|a:hover {.*?}|white-space: .*?;|font-family:.*?;|function\s+s|window.location.href\s+=\s+".*?"|return\s+false;| var _sedoq\s+=\s+_sedoq|_sedoq.partnerid\s+=\s+''316085'';| _sedoq.locale\s+=\s+''zh-cn'';|var\s+s\s+=\s+document.createElement|s.type\s+=\s+''text/javascript'';|s.async\s+=\s+true;|s.src\s+=\s+''.*?'';|var\s+f\s+=\s+document.getElementsByTagName|f.parentNode.insertBefore|/.*?/|pre\s+{|word-wrap:\s+break-word;|}|\s*\(str1\){|\s+\+\s+str1;|\s+\|\s+\|\|\s+{;|\s+\|\|\s+{;|_sedoq.partnerid|\s+=|''316085''|\s+'';|\s+enter\s+your\s+partner\s+id|_sedoq.locale\s+=\s+|zh-cn|language\s+locale|\(function\(\)\s+{|\[0\];|s.type|text/javascript|script|s,\s+f|document.getElementById\(.*?\)|.style.marginLeft|=window|\|\||\s+{|;|en-us,|en-uk,|de-de,|es-er-fr,|pt-br,|\s+.innerWidth2|es-|er-|fr|.innerWidth2|er|-,')
        tih = re.sub(comp, '', wsd)
        tih_list = tih.split('\n')
        tih_list = tih_list[46:-12]
        # print(tih_list)

        res1_list = []
        number = 0
        for i in tih_list:
            if i != "":
                res1_list.append(i)

        step = 7
        res2_list = [res1_list[i:i + step] for i in range(0, len(res1_list), step)]
        for i in res2_list:
            number +=1
        number_list = list(range(1, number + 1))

        dict_res = dict(zip(number_list, res2_list))
        print('dict:-----', dict_res)
    except:
        pass

if __name__ == '__main__':
    gethttps("jwt1399.top")