from .encode import sign
import json
import urllib.parse
import urllib.request

secret = '' # 钉钉密钥

def send(data):
    info = sign(secret)
    url = ""
    header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
    send_data = json.dumps(data)  # 将字典类型数据转化为json格式
    send_data = send_data.encode("utf-8")  # 编码为UTF-8格式
    request = urllib.request.Request(url=url, data=send_data, headers=header)  # 发送请求
    opener = urllib.request.urlopen(request)  # 将请求发回的数据构建成为文件格式
    print(opener.read())  # 打印返回的结果
