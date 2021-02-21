import requests
import re
import random
#import onetimepass as otp
from time import sleep
from urllib import parse
import os
from getver1 import Getver
import logging

class Autoreply:
    result=None
    over=False
    flag=False
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    loginurl = 'https://t66y.com/login.php'
    url='https://t66y.com/thread0806.php?fid=7&search=today'
    posturl='https://t66y.com/post.php?'
    indexurl='https://t66y.com/index.php'
    black_list=['htm_data/0612/9/5877.html',
                'htm_data/2102/7/2520305.html',
                'htm_data/2005/7/2404767.html',
                'htm_data/2003/7/3832698.html',
                'htm_data/1602/7/37458.html',
                'htm_data/1502/7/1331010.html']
    s=requests.Session()
    headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    headers1={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'https://t66y.com/login.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    headers2={
        'Host': 't66y.com',
        'Origin': 'null',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    def __init__(self,user,password):
        self.user= user.encode('gb18030')
        self.password= password

    def login1(self):
        sleep(2)
        Err=None
        data={
                'pwuser': self.user,
                'pwpwd':  self.password,
                'hideid': '0',
                'cktime': '0',
                'forward': 'https://t66y.com/post.php?',
                'jumpurl': 'https://t66y.com/post.php?',
                'step': '2'
        }
        login=self.s.post(self.loginurl,headers=self.headers,data=data)
        self.cookies=login.cookies
        login=login.text.encode('iso-8859-1').decode('gbk')
        if login.find('登录尝试次数过多')!=-1:
            return '登录尝试次数过多,需输入验证码'
        if login.find('您已經順利登錄')!=-1:
            return '您已經順利登錄'

    def getverwebp(self):
        code=random.uniform(0,1)
        code=round(code,16)
        vercodeurl='https://t66y.com/require/codeimg.php?'+str(code)
        image=self.s.get(vercodeurl,headers=self.headers1)
        f=open('image.webp','wb')
        f.write(image.content)
        f.close()

    def inputvercode(self,vercode):
        sleep(2)
        vercode=vercode
        data={
            'validate': vercode
        }
        login=self.s.post(self.loginurl,data=data,headers=self.headers1)
        login=login.text.encode('iso-8859-1').decode('gbk')
        if login.find('驗證碼不正確')!=-1:
            Err='验证码不正确，请重新输入'
            return Err

    def gettodaylist(self):
        pat=('htm_data/\w+/\w+/\w+.html')
        con=self.s.get(self.url,headers=self.headers)
        con = con.text.encode('iso-8859-1').decode('gbk','ignore')
        match=re.findall(pat,con)
        self.match=match
        qiuzhutie=con.find('求片求助貼')
        qiuzhutie=con[qiuzhutie-100:qiuzhutie]
        if re.findall(pat,qiuzhutie)!=[]:
            qiuzhutielink=re.findall(pat,qiuzhutie)
        else:
            qiuzhutielink=['no']
            self.match.append('no')
        self.logger.debug('求助帖链接是:'+qiuzhutielink[0])
        self.black_list.append(qiuzhutielink[0])
        try:
            for data in self.black_list:
                self.match.remove(data)
        except:
            print('移除失败，知道因为啥。。。')
            pass

    def getonelink(self):
        for m in range(len(self.match)):
            geturl = 'https://t66y.com/'+self.match[m]
            page = self.s.post(geturl,headers=self.headers)
            page = page.text.encode('iso-8859-1').decode('gbk')
            if page.find('下一頁')!=-1 and page.find('求片求助貼')==-1 and page.find('Diss')==-1 and page.find('valen')==-1:
                break
            sleep(2)
        self.geturl=geturl
        tid=self.match[m][16:len(self.match[m])-5]
        self.tid=tid
        self.match.remove(self.match[m])
        self.debug('请求链接是: '+geturl)

    def browse(self):
        res=requests.get(url=self.geturl,headers=self.headers,cookies=self.cookies)
        #res=res.text.encode('iso-8859-1').decode('gbk')
        #print(res)

    #不知道啥用，留着吧
    def getmatch(self):
        sleep(2)
        get=requests.get(self.geturl,headers=self.headers,cookies=self.cookies)
        sleep(2)
        get=get.text.encode('iso-8859-1').decode('gbk')
        pat='<b>本頁主題:</b> .*</td>'
        res=re.search(pat,get)
        res=res.group(0).replace('<b>本頁主題:</b> ','').replace('</td>','')
        res='Re:'+res
        self.res=res
        #print(res)

    def getreply(self):
        #自定义回复内容，记得修改随机数
        reply=['感谢分享','多谢聚聚分享','谢谢分享','后排支持','好帖支持']
        reply_m=random.randint(0,4)
        reply_news=reply[reply_m]
        self.reply_news=reply_news.encode('gb18030')
        self.logger.debug("本次回复内容是:"+reply_news)

    #暂时没用，看以后了
    # def encodepost(self):
    #     res=self.res.encode('gbk')
    #     res=parse.quote(res)
    #     self.encoderesult=res
    #     print(self.encoderesult)
    #     reply_news=self.reply_news.encode('gbk')
    #     reply_news=parse.quote(reply_news)
    #     self.encoderesult=res
    #     self.encodereply=reply_news
    #     #print(self.encodereply)

    def postreply(self):
        data={
            'atc_usesign':'1',
            'atc_convert':'1',
            'atc_autourl': '1',
            'atc_title': self.res ,
            'atc_content': self.reply_news ,
            'step': '2',
            'action': 'reply',
            'fid': '7',
            'tid': self.tid ,
            'atc_attachment': 'none',
            'pid':'',
            'article':'',
            'touid':'',
            'verify':'verify'
        }
        post=requests.post(self.posturl,data=data,headers=self.headers2,cookies=self.cookies)
        post = post.text.encode('iso-8859-1').decode('gbk')
        if post.find('發貼完畢點擊')!=-1:
            status='回复成功'
            return status
        if post.find('所屬的用戶組')!=-1:
            status='今日已达上限'
            return status

    def getnumber(self):
        sleep(2)
        index=requests.get(self.indexurl,headers=self.headers,cookies=self.cookies)
        index = index.text.encode('iso-8859-1').decode('gbk')
        pat='共發表帖子: \d{1,5}'
        num=re.search(pat,index).group(0)
        num=num.replace('共發表帖子: ','')
        return num
    
    def debug(self,content):
        self.logger.debug(content)

if __name__ == "__main__":
    n=0
    success=None
    suc=False
    user= os.environ["USER"]
    password= os.environ["PASSWORD"]
    auto=Autoreply(user,password)

    while success is None:
        au=auto.login1()
        if au=='登录尝试次数过多,需输入验证码':
            auto.debug('登录尝试次数过多,需输入验证码')
            auto.getverwebp()
            getcd=Getver()
            vercode=getcd.getcode()
            auto.debug(vercode)
            while auto.inputvercode(vercode)=='验证码不正确，请重新输入':
                auto.debug('验证码不正确，请重新输入')
                auto.getverwebp()
                vercode=getcd.getcode()
                auto.debug(vercode)
        elif au=='您已經順利登錄':
            auto.debug('登录成功')
            success = True
            au=''
        else:
            auto.debug('error')
            exit()
            
    m=auto.getnumber()
    auto.gettodaylist()
    #回复
    while n<10 and suc is False:
        try:
            auto.debug("当前在第"+str(n+1)+'个。')
            auto.getonelink()
            auto.browse()
            auto.getreply()
            auto.getmatch()
            au=auto.postreply()
            if au=='回复成功':
                auto.debug('回复成功')
            elif au=='今日已达上限':
                auto.debug('回复失败，今日次数已达10次')
                suc=True
            else:
                while 1:
                    auto.debug('1024限制！！！')
                    sleep(60)
                    auto.debug('休眠完成')
                    au=auto.postreply()
                    if au=='回复成功':
                        auto.debug('回复成功')
                        break
            if au=='回复成功':
                sleeptime=random.randint(900,960)
                n=n+1
                if n<10:
                    auto.debug('休眠'+str(sleeptime)+'s...')
                    sleep(sleeptime)
                    auto.debug('休眠完成')
        except:
            print('回复失败，重试')
    n=auto.getnumber()
    auto.debug('开始时发表帖子:'+m)
    auto.debug('结束时发表帖子:'+n)
    auto.debug('回复'+str(int(n)-int(m))+'次')
