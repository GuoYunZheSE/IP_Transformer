import urllib.request
import re
import urllib.parse
import urllib.error
import bs4
import os
import time
import random
import sys
import getopt


def __toHex(obj):
  if   obj == '': return ''
  elif obj == 0 or obj == '0' or obj == '00': return '00'
  if isinstance(obj, str):
    rehex = [str(hex(ord(s))).replace('0x','') for s in obj]
    return ','.join(rehex)
  elif isinstance(obj, int):
    num = str(hex(obj)).replace('0x', '')
    return num if len(num)>1 else '0'+num # 如果是一位数则自动补上0，7为07，e为0e

def regIESettings(op, noLocal=False, ip='', pac=''):
  '''
    # 根据需求生成Windows代理设置注册表的.reg文件内容
    # DefaultConnectionSettings项是二进制项
    # 而具体这个二进制文件怎么解析，在收藏的PDF中有详细解释。
  '''
  if not op : return
  # 如果是设置IP代理的模式 则检查IP地址的有效性(允许为空，但不允许格式错误)
  if 'Proxy' in op and not ip == '':
    # if len(extractIp(ip))==0
    if 1 > len(re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*:{0,1}\s*([0-9]{1,5}){0,1}',ip)) :
      print ('---Unexpected IP Address:%s---'%ip)
      return
  options = {'On':'0F','Off':'01','ProxyOnly':'03','PacOnly':'05','ProxyAndPac':'07','D':'09','DIP':'0B','DS':'0D'}
  if op == 'Off':
    reg_value = '46,00,00,00,00,00,00,00,01'
  else:
    switcher = options.get(op)
    if not switcher:
      print ('\n---Unexpected Option. Please check the value after [-o]---\n')
      return
    skipLocal = '07,00,00,00,%s'%__toHex('<local>') if noLocal else '00'
    reg_value = '46,00,00,00,00,00,00,00,%(switcher)s,00,00,00,%(ipLen)s,00,00,00,%(ip)s00,00,00,%(skipLocal)s,21,00,00,00%(pac)s' % ({ 'switcher':switcher,'ipLen':__toHex(len(ip)),'ip':__toHex(ip)+',' if ip else '','infoLen':__toHex(len('<local>')),'skipLocal':skipLocal,'pac':','+__toHex(pac) if pac else '' })
  settings = 'Windows Registry Editor Version 5.00\n[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections]\n"DefaultConnectionSettings"=hex:%s' % reg_value
  # print 'Using proxy address: %s' % ip
  # print (op, ip, pac)
  # print (options[op] +'\n'+ __toHex(ip) +'\n'+ __toHex(pac))
  # print (settings)
  # === 生成reg文件并导入到注册表中 ===
  filePath = '%s\DefaultConnectionSettings.reg'%os.getcwd()
  with open(filePath, 'w') as f:
    f.write( settings )
  cmd = 'reg import "%s"' %filePath
  result  = os.popen(cmd)
  if len(result.readlines()) < 2 :
    print ('--- 老公做完啦，要亲亲要抱抱~~ ---')
  return


class IP_Transformer:
    def __init__(self,city,number):
        self.city=city
        self.ip_list=[]
        self.ip_number=number

    def get_ip_list_XC(self,obj,j):
        ip_text = obj.findAll('tr', {'class': 'odd'})  # 获取带有IP地址的表格的所有行
        for i in range(len(ip_text)):
            ip_tag = ip_text[i].findAll('td')
            if self.city in ip_tag[3].get_text().strip('\n'):
                temp = []
                ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()  # 提取出IP地址和端口号
                temp.append(ip_port)
                temp.append(ip_tag[3].get_text().strip('\n'))
                temp.append(ip_tag[8].get_text())
                proxy_handler = urllib.request.ProxyHandler({"http": ip_port})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
                try:
                    html = urllib.request.urlopen('http://www.baidu.com')
                    self.ip_list.append(temp)
                except Exception:
                    print('{} is not valid'.format(temp[0]))
                    continue
                except TimeoutError:
                    print('{} is not valid'.format(temp[0]))
                    try:
                        print('{} is not valid'.format(temp[0]))
                        continue
                    except urllib.error.URLError:
                        print('{} is not valid'.format(temp[0]))
                        continue
                except urllib.error.HTTPError:
                    print('{} is not valid'.format(temp[0]))
                    continue
                except urllib.error.URLError:
                    print('{} is not valid'.format(temp[0]))
                    continue
        print("第{}次共收集到了{}个{}的代理IP".format(j,len(self.ip_list), self.city))
        print(self.ip_list)

    def get_ip_list_KD(self,obj,j):
        ip_text = obj.findAll('tr')  # 获取带有IP地址的表格的所有行
        for i in range(1,len(ip_text)):
            ip_tag = ip_text[i].findAll('td')
            if self.city in ip_tag[4].get_text():
                temp = []
                ip_port = ip_tag[0].get_text() + ':' + ip_tag[1].get_text()  # 提取出IP地址和端口号
                temp.append(ip_port)
                temp.append(ip_tag[4].get_text())
                temp.append(ip_tag[5].get_text())
                proxy_handler = urllib.request.ProxyHandler({"http": ip_port})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
                try:
                    html = urllib.request.urlopen('http://www.baidu.com')
                    self.ip_list.append(temp)
                except Exception:
                    print('{} is not valid'.format(temp[0]))
                    continue
                except TimeoutError:
                    print('{} is not valid'.format(temp[0]))
                    try:
                        print('{} is not valid'.format(temp[0]))
                        continue
                    except urllib.error.URLError:
                        print('{} is not valid'.format(temp[0]))
                        continue
                except urllib.error.HTTPError:
                    print('{} is not valid'.format(temp[0]))
                    continue
                except urllib.error.URLError:
                    print('{} is not valid'.format(temp[0]))
                    continue
        print("第{}次共收集到了{}个{}的代理IP".format(j,len(self.ip_list), self.city))
        print(self.ip_list)


    def parse_ip_web_XC(self):
        i=1
        while self.ip_list.__len__()<self.ip_number:
            time.sleep(2)
            if i==1:
                url = 'http://www.xicidaili.com/nt'
            else:
                url = 'http://www.xicidaili.com/nt/{}'.format(i)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN, zh;q=0.8',
                'Pragma': 'no - cache',
                'Cache - Control': 'no - cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            bsObj = bs4.BeautifulSoup(response, 'lxml')  # 解析获取到的html
            self.get_ip_list_XC(bsObj,i)
            i+=1

    def parse_ip_web_KD(self):
        i=1
        while self.ip_list.__len__()<self.ip_number:
            time.sleep(1)
            url = 'https://www.kuaidaili.com/free/intr/{}/'.format(i)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN, zh;q=0.8',
                'Pragma': 'no - cache',
                'Cache - Control': 'no - cache',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            bsObj = bs4.BeautifulSoup(response, 'lxml')  # 解析获取到的html
            self.get_ip_list_KD(bsObj,i)
            i+=1

    def get_random_ip(self):
        random.seed(time.localtime().tm_sec)
        random_ip = random.choice(self.ip_list)[0]
        print('Using Proxy:{}'.format(random_ip))
        return random_ip

if __name__ == '__main__':
    while True:
        command = input('想干嘛？\nA：开启代理 B：关闭代理 C: 退出\n<<')
        if command == 'A':
            city = input('输入代理城市，例如：上海\n<<')
            print('好哒，辛勤工作中~~')
            IP_T = IP_Transformer(city, 5)
            line=input('要选一下线路喔，不同的线路速度可能不太一样~\n A:线路一(推荐) B:线路二\n<<')
            if line=='A':
                IP_T.parse_ip_web_KD()
            else:
                IP_T.parse_ip_web_XC()
            ip = IP_T.get_random_ip()
            pac = ' '
            regIESettings(op='On', ip=ip, pac=pac, noLocal=False)
        if command == 'B':
            regIESettings(op='Off', ip='', pac='', noLocal=False)
        if command=='C':
            exit(0)