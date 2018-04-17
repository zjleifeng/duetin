#!/usr/bin/env python
# encoding: utf-8

"""
@author: zj
@site  :
@file: aliSTStoken.py
@time: 2018/4/12 下午6:11
@SOFTWARE:PyCharm
"""
from khafre.utils.json_response import json_resp

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2
from khufu.settings.defaults import access_key_secret,access_key_id,endpoint,sts_role_arn


# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, endpoint, sts_role_arn):
    assert '<' not in param, '请设置参数：' + param


class StsToken(object):
    """AssumeRole返回的临时用户密钥
    :param str access_key_id: 临时用户的access key id
    :param str access_key_secret: 临时用户的access key secret
    :param int expiration: 过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
    :param str security_token: 临时用户Token
    :param str request_id: 请求ID
    """
    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''


def fetch_sts_token(access_key_id, access_key_secret, role_arn):
    """子用户角色扮演获取临时用户的密钥
    :param access_key_id: 子用户的 access key id
    :param access_key_secret: 子用户的 access key secret
    :param role_arn: STS角色的Arn
    :return StsToken: 临时用户密钥
    """
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    req = AssumeRoleRequest.AssumeRoleRequest()

    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('oss-python-sdk-example')

    body = clt.do_action(req)

    j = json.loads(body)

    # token = StsToken()
    #
    # token.access_key_id = j['Credentials']['AccessKeyId']
    # token.access_key_secret = j['Credentials']['AccessKeySecret']
    # token.security_token = j['Credentials']['SecurityToken']
    # token.request_id = j['RequestId']
    # token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')

    return j


# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行

def alistsauth(request):
    token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
    # auth = oss2.StsAuth(token.access_key_id, token.access_key_secret, token.security_token)
    return token





# bucket_name = 'duetin'
# bucket = oss2.Bucket(auth, endpoint, bucket_name)
#
# with open('/tmp/logo.png', 'rb') as fileobj:
#     bucket.put_object('remote.png', fileobj)