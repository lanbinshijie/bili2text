# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib.parse

lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        """
        生成签名信息
        """
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg，使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = signa.decode('utf-8')
        return signa

    def upload(self):
        """
        上传音频文件
        """
        print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {
            'appId': self.appid,
            'signa': self.signa,
            'ts': self.ts,
            'fileSize': str(file_len),
            'fileName': file_name,
            'duration': '200'
        }
        print("upload参数：", param_dict)
        with open(upload_file_path, 'rb') as f:
            data = f.read()

        url = lfasr_host + api_upload + "?" + urllib.parse.urlencode(param_dict)
        response = requests.post(url=url,
                                 headers={"Content-type": "application/json"},
                                 data=data)
        print("upload_url:", response.request.url)
        result = response.json()
        print("upload resp:", result)
        return result

    def get_result(self):
        """
        获取转写结果
        """
        uploadresp = self.upload()
        if uploadresp['code'] != '000000':
            print("上传失败:", uploadresp['message'])
            return None

        orderId = uploadresp['content']['orderId']
        param_dict = {
            'appId': self.appid,
            'signa': self.signa,
            'ts': self.ts,
            'orderId': orderId,
            'resultType': "transfer,predict"
        }
        print("\n查询部分：")
        print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            url = lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict)
            response = requests.post(url=url,
                                     headers={"Content-type": "application/json"})
            result = response.json()
            print(result)
            if result['code'] != '000000':
                print("获取结果失败:", result['message'])
                return None
            status = result['content']['orderInfo']['status']
            print("status=", status)
            if status == 4:
                break
            time.sleep(5)
        print("get_result resp:", result)
        return result


def doRequest(folder, filename):
    """
    发起请求并获取转写结果
    """
    api = RequestApi(
        appid="您的appid",  # 请填写您自己的appid
        secret_key="您的secret_key",  # 请填写您自己的secret_key
        upload_file_path=os.path.join("audio", "slice", folder, filename)
    )

    res = api.get_result()
    if res is None:
        print("获取结果失败。")
        return None
    print(res)
    return res


def extract_and_format_transcription_from_dict(json_data):
    """
    提取并格式化转写结果为段落
    """
    # 提取转写结果
    order_result_str = json_data.get("content", {}).get("orderResult", "{}")
    order_result = json.loads(order_result_str)

    # 解析转写结果
    sentences = []
    for lattice in order_result.get("lattice", []):
        json_1best_str = lattice.get("json_1best", "{}")
        json_1best = json.loads(json_1best_str)

        # 提取并处理每个词
        for rt in json_1best.get("st", {}).get("rt", []):
            sentence = ''.join([c["w"] for ws in rt.get("ws", []) for c in ws.get("cw", [])])
            sentences.append(sentence)

    # 将句子拼接成段落
    paragraph = ' '.join(sentences)
    return paragraph