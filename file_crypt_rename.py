import base64
from Cryptodome.Cipher import AES

def add_to_16(s):
    while len(s) % 16 != 0:
        s += b'\0'
    return s
key = input("请输入:   秘钥（16位纯数字）    \n")
filename = input("请输入:   文件名.后缀    \n")
with open (filename,'rb') as f:
    text = f.read()

aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式
dic = {'a':'已加密','b':'已解密'}
ende = input("请选择:   a.加密  b.解密    \n")
if ende == "a":
    text = base64.encodebytes(aes.encrypt(add_to_16(text))) # 加密
if ende == "b":
    text = aes.decrypt(base64.decodebytes(text)).rstrip(b'\0')  # 解密

with open ((filename+dic[ende]),'wb') as f:
    f.write(text)
