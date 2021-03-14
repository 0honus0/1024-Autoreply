import requests
import re
import random
import onetimepass as otp
from time import sleep
from urllib import parse
import os
from getver import Getver
from multiprocessing import Pool

class Autoreply:
    result=None
    over=False
    flag=False
    loginurl = 'http://t66y.com/login.php'
    url='http://t66y.com/thread0806.php?fid=7&search=today'
    headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    headers1={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/login.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    def __init__(self,user,password,secret):
        self.user= user.encode('gb18030')
        self.password= password
        self.secret =secret
        self.s=requests.Session()

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

    def getcookies(self):
        return self.cookies

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
            print('置顶帖为:'+black)
            black_list.append(black)

        match=re.findall(pat,con)
        self.match=match
        try:
            for data in black_list:
                self.match.remove(data)
        except:
            print('移除失败，若出现此信息，请立即停止运行该脚本，删除定时任务中的触发，等待更新')
            os._exit(0)
        return self.match

    @staticmethod
    def getonelink(todaylist):
        geturl=''
        m=random.randint(0,len(todaylist)-1)
        geturl='http://t66y.com/'+todaylist[m]
        tid=todaylist[m][16:len(todaylist[m])-5]
        todaylist.remove(todaylist[m])
        #print('请求链接是: '+geturl)
        return geturl,tid

    @staticmethod
    def browse(geturl,cookies):
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        res=requests.get(url=geturl,headers=headers,cookies=cookies)
        #res=res.text.encode('iso-8859-1').decode('gbk')

    @staticmethod
    def getmatch(geturl,cookies):
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        sleep(2)
        get=requests.get(geturl,headers=headers,cookies=cookies)
        sleep(2)
        get=get.text.encode('iso-8859-1').decode('gbk')
        pat='<b>本頁主題:</b> .*</td>'
        res=re.search(pat,get)
        res=res.group(0).replace('<b>本頁主題:</b> ','').replace('</td>','')
        res='Re:'+res
        return res
        #print(res)

    @staticmethod
    def getreply():
        #自定义回复内容，记得修改随机数
        reply=['感谢分享','感谢你的分享','谢谢分享','多谢分享','感谢作者的分享','谢谢坛友分享','内容精彩','的确如此','感谢分享','涨知识了','很有意思']
        reply_m=random.randint(0,10)
        reply_news=reply[reply_m]
        print('本次回复消息是:'+reply_news)
        reply_news=reply_news.encode('gb18030')
        return  reply_news

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

    @staticmethod
    def postreply(cookies,res,reply_news,tid):
        headers={
        'Host': 't66y.com',
        'Origin': 'null',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        posturl='http://t66y.com/post.php?'
        data={
            'atc_usesign':'1',
            'atc_convert':'1',
            'atc_autourl': '1',
            'atc_title': res ,
            'atc_content': reply_news ,
            'step': '2',
            'action': 'reply',
            'fid': '7',
            'tid': tid ,
            'atc_attachment': 'none',
            'pid':'',
            'article':'',
            'touid':'',
            'verify':'verify'
        }
        post=requests.post(posturl,data=data,headers=headers,cookies=cookies)
        post = post.text.encode('iso-8859-1').decode('gbk')
        if post.find('發貼完畢點擊')!=-1:
            status='回复成功'
            return status
        if post.find('所屬的用戶組')!=-1:
            status='今日已达上限'
            return status

    @staticmethod
    def getnumber(cookies):
        indexurl='http://t66y.com/index.php'
        headers={
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        sleep(2)
        index=requests.get(indexurl,headers=headers,cookies=cookies)
        index = index.text.encode('iso-8859-1').decode('gbk')
        pat='共發表帖子: \d{1,5}'
        num=re.search(pat,index).group(0)
        num=num.replace('共發表帖子: ','')
        return num

    @staticmethod
    def main(cookieslist,todaylist,ge):
        #回复
        n=0
        cookies=cookieslist[ge]
        m=Autoreply.getnumber(cookies)
        suc=False
        print('第'+str(ge+1)+'个账号开始时发表帖子:'+m)
        while n<10 and suc is False:
            try:
                au=''
                print('第'+str(ge+1)+'个账号当前在回复第'+str(n+1)+'个。')
                geturl,tid=Autoreply.getonelink(todaylist)
                reply_news=Autoreply.getreply()
                res=Autoreply.getmatch(geturl,cookies)
                sleeptime=random.randint(1024,2048)
                au=Autoreply.postreply(cookies,res,reply_news,tid)
                if au=='回复成功':
                    print('第'+str(ge+1)+'个账号回复成功')
                    n=n+1
                    print('第'+str(ge+1)+'个账号休眠'+str(sleeptime)+'s...')
                    Autoreply.browse(geturl,cookies)
                    sleep(sleeptime)
                    print('第'+str(ge+1)+'个账号休眠完成')
                elif au=='今日已达上限':
                    print('第'+str(ge+1)+'个账号回复失败，今日次数已达10次')
                    suc=True
                else:
                    print('第'+str(ge+1)+'个账号1024限制或者被禁言！！！')
                    print('第'+str(ge+1)+'个账号休眠'+str(sleeptime)+'s...')
                    sleep(sleeptime)
                    print('第'+str(ge+1)+'个账号休眠完成')
            except:
                print('第'+str(ge+1)+'个账号回复失败，重试')
                sleep(60)
        n=Autoreply.getnumber(cookies)
        print('第'+str(ge+1)+'个账号开始时发表帖子:'+m)
        print('第'+str(ge+1)+'个账号结束时发表帖子:'+n)
        print('第'+str(ge+1)+'个账号回复'+str(int(n)-int(m))+'次')

if __name__ == "__main__":
    n=0
    cookieslist=[]
    todaylist=[]
    user= os.environ["USER"]
    password= os.environ["PASSWORD"]
    secret =os.environ["SECRET"]

    userlist=user.split()
    passwordlist=password.split()
    secretlist=secret.split()

    if len(userlist)!=len(passwordlist) and len(passwordlist)!=len(secretlist):
        print('参数个数不匹配，请检查环境变量设置是否正确')
        os._exit(0)
    else:
        print('检测到',len(userlist),'个账号')


    count=0
    while count<len(userlist):
        success=None
        auto=Autoreply(userlist[count],passwordlist[count],secretlist[count])
        while success is None:
            au=auto.login1()
            if au=='登录尝试次数过多,需输入验证码':
                print('登录尝试次数过多,需输入验证码')
                auto.getverwebp()
                getcd=Getver()
                vercode=getcd.getcode()
                print(vercode)
                while auto.inputvercode(vercode)=='验证码不正确，请重新输入':
                    print('验证码不正确，请重新输入')
                    auto.getverwebp()
                    vercode=getcd.getcode()
                    print(vercode)
                if auto.login1()=='賬號已開啟兩步驗證':
                    if auto.login2()=='已經順利登錄':
                        print('登录成功')
                        success = True
                        au=''
            else:
                if au=='賬號已開啟兩步驗證':
                    if auto.login2()=='已經順利登錄':
                        print('登录成功')
                        success = True
                        au=''
        cookies=auto.getcookies()
        cookieslist.append(cookies)
        count+=1
    print('cookies获取完成')
    todaylist=auto.gettodaylist()
    p=Pool(len(userlist))
    for i in range(len(userlist)):
        res=p.apply_async(Autoreply.main,args=[cookieslist,todaylist,i])
        print('第',str(i+1),'个进程启动.。。')
    p.close()
    p.join()
    print(res.get())          #查看错误信息
    print('完成')
