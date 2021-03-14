import requests
import re
import random
import onetimepass as otp
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
    loginurl = 'http://t66y.com/login.php'
    url='http://t66y.com/thread0806.php?fid=7&search=today'
    posturl='http://t66y.com/post.php?'
    indexurl='http://t66y.com/index.php'
    s=requests.Session()
    headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    headers1={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/login.php',
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

    def __init__(self,user,password,secret):
        self.user= user.encode('gb18030')
        self.password= password
        self.secret =secret

    def login1(self):
        sleep(2)
        Err=None
        data={
                'pwuser': self.user,
                'pwpwd':  self.password,
                'hideid': '0',
                'cktime': '0',
                'forward': 'http://t66y.com/post.php?',
                'jumpurl': 'http://t66y.com/post.php?',
                'step': '2'
        }
        login=self.s.post(self.loginurl,headers=self.headers,data=data)
        login=login.text.encode('iso-8859-1').decode('gbk')
        if login.find('登录尝试次数过多')!=-1:
            Err='登录尝试次数过多,需输入验证码'
            return Err
        elif login.find('賬號已開啟兩步驗證')!=-1:
            Err='賬號已開啟兩步驗證'
            return Err

    def login2(self):
        sleep(2)
        my_token = otp.get_totp(self.secret)
        data={
        'step': '2',
        'cktime': '0',
        'oneCode': str(my_token)
        }
        login=self.s.post(self.loginurl,headers=self.headers,data=data)
        self.cookies=login.cookies
        login=login.text.encode('iso-8859-1').decode('gbk')
        if login.find('您已經順利登錄')!=-1:
            res='已經順利登錄'
            self.s.close()
            return res

    def getverwebp(self):
        code=random.uniform(0,1)
        code=round(code,16)
        vercodeurl='http://t66y.com/require/codeimg.php?'+str(code)
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
        black_list=[]
        pat=('htm_data/\w+/\w+/\w+.html')
        con=self.s.get(self.url,headers=self.headers)
        con = con.text.encode('iso-8859-1').decode('gbk','ignore')
        theme=con.find('普通主題')
        top=con[:theme]
        pin=re.findall(pat,top)
        for black in pin:
            auto.debug('置顶帖为:'+black)
            black_list.append(black)

        match=re.findall(pat,con)
        self.match=match
        try:
            for data in black_list:
                self.match.remove(data)
        except:
            auto.debug('移除失败，若出现此信息，请立即停止运行该脚本，删除定时任务中的触发，等待更新')
            os._exit(0)

    def getonelink(self):
        geturl=''
        m=random.randint(0,len(self.match)-1)
        geturl='http://t66y.com/'+self.match[m]
        self.geturl=geturl
        tid=self.match[m][16:len(self.match[m])-5]
        self.tid=tid
        self.match.remove(self.match[m])
        #print('请求链接是: '+geturl)

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
        reply=['感谢分享','感谢你的分享','谢谢分享','多谢分享','感谢作者的分享','谢谢坛友分享','内容精彩','的确如此','感谢分享','涨知识了','很有意思']
        reply_m=random.randint(0,10)
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
    secret =os.environ["SECRET"]
    auto=Autoreply(user,password,secret)

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
            if auto.login1()=='賬號已開啟兩步驗證':
                if auto.login2()=='已經順利登錄':
                    auto.debug('登录成功')
                    success = True
                    au=''
        else:
            if au=='賬號已開啟兩步驗證':
                if auto.login2()=='已經順利登錄':
                    auto.debug('登录成功')
                    success = True
                    au=''
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
            sleeptime=random.randint(1024,2048)
            au=auto.postreply()
            if au=='回复成功':
                auto.debug('回复成功')
                n=n+1
                auto.debug('休眠'+str(sleeptime)+'s...')
                sleep(sleeptime)
                auto.debug('休眠完成')
            elif au=='今日已达上限':
                auto.debug('回复失败，今日次数已达10次')
                suc=True
            else:
                auto.debug('1024限制！！！')
                auto.debug('休眠'+str(sleeptime)+'s...')
                sleep(sleeptime)
                auto.debug('休眠完成')
        except:
            auto.debug('回复失败，重试')
    n=auto.getnumber()
    auto.debug('开始时发表帖子:'+m)
    auto.debug('结束时发表帖子:'+n)
    auto.debug('回复'+str(int(n)-int(m))+'次')
