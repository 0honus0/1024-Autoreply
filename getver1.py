# encoding:utf-8
import requests
import base64
from PIL import Image
import os
import json

class Getver:
    def getcode(self):
        im=Image.open('image.webp')
        im.save('image.png')
        f=open('image.png','rb')
        image=base64.b64encode(f.read())
        host='http://api.ttshitu.com/base64'
        headers={
            'Content-Type':'application/json;charset=UTF-8'
        }
        data={
            'username': os.environ["CODEUSER"] ,
            'password': os.environ["CODEPASS"] ,
            'image':image.decode('utf-8')
        }
        res=requests.post(url=host,data=json.dumps(data))
        res=res.text
        res=json.loads(res)
        res=res['data']['result']
        return res