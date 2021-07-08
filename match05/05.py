import requests
import base64
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
"""
2021.7.8测试有效
"""
def gettime():
    return str(int(time.time()))+'000'
 
def main():
    # m为12位时间截，末尾增加一个0，除去最后一位后base64作为ecb的key
    # f为10位时间截，末尾增加三个0
    m = str(int(time.time()*1000))
    f = gettime()
    # 前面push 进数组的因为没有传递加密前值给服务器没法校验写死即可
    data = "e46ae7873182926b81cf81a88c8ed2d0,ea39ed5db9fa45984b7ce00a0a2e5778,54f203edfb65f05f0d4da5db9762ed34,007d11b26303aed47bc4cfeb5b46be5b,"
    nodejs = os.popen('node 05 '+m)
    cm = nodejs.read().replace('\n', '')
    print(cm)
    data += cm
    nodejs.close()
    key = base64.b64encode(m[:-1].encode())
    cryptor = AES.new(key=key, mode=AES.MODE_ECB)
    data = base64.b64encode(cryptor.encrypt(pad(data.encode(), AES.block_size))).decode()
    print(data)
    headers = {
        'cookie': 'm='+cm+'; RM4hZBv0dDon443M='+data+'; tk=964448564923972225; sessionid=wsrn0le3dpqkuv1pm9q6h99tu5yqrqgw;',
        'user-agent':'yuanrenxue.project'
    }
    popularitylist = []
    
    for page in range(1, 6):
        url = 'http://match.yuanrenxue.com/api/match/5?page='+str(page)+'&m='+m+'&f='+f
        response = requests.get(url, headers=headers)
        print(response.text)
        for each in response.json()['data']:
            popularitylist.append(each['value'])
    popularitylist.sort()
    sums = sum(popularitylist[-5:])
    print(sums)
    
 
if __name__ == '__main__':
    main()