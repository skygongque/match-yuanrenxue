import requests
import base64
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
 
def gettime():
    return str(int(time.time()))+'000'
 
def main():
    # m为12位时间截，末尾增加一个0，除去最后一位后base64作为ecb的key
    # f为10位时间截，末尾增加三个0
    m = str(int(time.time()*1000))
    f = gettime()
    # 前面push 进数组的因为没有传递加密前值给服务器没法校验写死即可
    data = '5ebb09ca3d0199732a48ec64851405f9,5ebb09ca3d0199732a48ec64851405f9,5ebb09ca3d0199732a48ec64851405f9,5ebb09ca3d0199732a48ec64851405f9,'
    nodejs = os.popen('node 05 '+m)
    cm = nodejs.read().replace('\n', '')
    data += cm
    nodejs.close()
    key = base64.b64encode(m[:-1].encode())
    cryptor = AES.new(key=key, mode=AES.MODE_ECB)
    data = base64.b64encode(cryptor.encrypt(pad(data.encode(), AES.block_size))).decode()
    headers = {
        'cookie': 'm='+cm+'; RM4hZBv0dDon443M='+data,
        'user-agent':'yuanrenxue.project'
    }
    for page in range(1, 6):
        url = 'http://match.yuanrenxue.com/api/match/5?page='+str(page)+'&m='+m+'&f='+f
        response = requests.get(url, headers=headers)
        print(response.text)
    
 
if __name__ == '__main__':
    main()