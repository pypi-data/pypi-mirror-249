#!/usr/bin/env python3

import json
import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth


class Client:
    # 认证
    def __init__(self, base_url, private_token, key_id, secret_id):
        self.base_url = base_url
        self.private_token = private_token
        self.key_id = key_id
        self.secret_id = secret_id
        self.gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
        self.headers = self._headers()
        self.auth = self._get_auth()
        

    def _headers(self):
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": 'Token ' + self.private_token,
            'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
            'Date': datetime.datetime.utcnow().strftime(self.gmt_form)
        }

    def _get_auth(self):
        """
        认证
        :param KeyID:  The key ID
        :param SecretID:    The secret ID
        :return:
        """
        signature_headers = ['(request-target)', 'accept', 'date']
        return HTTPSignatureAuth(key_id=self.key_id, 
                                 secret=self.secret_id, 
                                 algorithm='hmac-sha256', 
                                 headers=signature_headers)
    
    # 获取所有用户
    def get_user_all(self):
        """
        获取所有用户
        :return:
        """
        url = self.base_url + '/api/v1/users/users/'
        response = requests.get(url, auth=self.auth, headers=self.headers)
        user_list = json.loads(response.text)
        count = 0
        for i in user_list:
            count += 1
            print(i)
        return count

    # 获取所有资产节点
    def get_node_all(self):
        """
        获取所有资产节点
        :return:
        """
        url = self.base_url + "/api/v1/assets/nodes/"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        node_list = json.loads(response.text)
        count = 0
        for i in node_list:
            count += 1
            # print(i)
        # print(count)
        return response.json()

    # 查看当前token（即admin）的所有资产
    def get_asset_all(self):
        """
        查看当前token（即admin）的所有资产
        :return:
        """
        url = self.base_url + "/api/v1/assets/assets/"
        response = requests.get(url, headers=self.headers, auth=self.auth).json()
        # node_list = json.loads(response.text)
        # count = 0
        # for i in node_list:
            # count += 1
            # print(i)
        # print(count)
        return response

    # 创建资产节点
    def assets_nodes_create(self, node_name):
        """
        创建资产节点
        :param node_name:
        :return:
        """
        node_data = {
            "value": node_name
        }
        url = self.base_url + "/api/v1/assets/nodes/"
        node_info = self.get_node_info(node_name)
        if node_info:  
            print("{name}已存在, id: {id}".format(name=node_name, id=node_info[0]["id"]))
        else:
            data = json.dumps(node_data)
            resp = requests.post(url, headers=self.headers, data=data)
            return resp.json()

    # 获取资产信息
    def get_assets_list_by_ip(self, ip):
        """
        根据ip获取资产信息
        :param ip:
        :return:
        """
        # url = self.base_url + "/api/v1/assets/assets/"
        url = self.base_url + f'/api/v1/assets/assets/suggestions/?address={ip}'
        response = requests.get(url, headers=self.headers)
        print(response.json())
        return response.json()

    # 查看资产节点信息
    def get_node_info(self, node_name):
        """
        查看资产节点信息
        :param node_name:   节点名称
        :return:
        """
        url = self.base_url + "/api/v1/assets/nodes/"
        response = requests.get(url, auth=self.auth, headers=self.headers, params={
            "value": node_name
        }).json()[0]['id']
        return response

    def create_asset(self, ip, hostname, node_name, comment, username, password):
        """
        创建资产机器
        :param ip:  ip地址
        :param hostname:   主机名
        :param node_id:   节点id
        :param comment: 备注
        :param username: 账号用户名
        :param password: 账号密码
        :return:    返回创建的资产信息
        """
        asset_Data = {
            "name": hostname,
            "address": ip,
            "platform": "1",
            "protocols": [
                {
                "name": "ssh",
                "port": 58422,
                },
                {
                    "name": "sftp",
                    "port": 58422
                }
            ],

                "accounts": [{
                    "username": username,
                    "secret_type": "password",
                    "secret": password
            }
            ],
            "is_active": True,
            "nodes": [self.get_node_info(node_name=node_name)],
            "comment": comment
        }
        # print(self.get_node_info(node_name=node_name))

        url = self.base_url + "/api/v1/assets/hosts/"
        data = json.dumps(asset_Data)
        response = requests.post(url, auth=self.auth, headers=self.headers, data=data)
        if response.status_code == 201:
            return '创建成功'
        else:
            raise NotImplementedError(f'未创建成功, 返回状态码: {requests.status_codes}')

    #获取组织信息
    def get_org_info(self):
        """
        获取组织信息
        :return:
        """
        url = self.base_url + "/api/v1/orgs/orgs/"
        response = requests.get(url, headers=self.headers)
        org_list = response.text
        print(org_list)
        for i in org_list.split("id"):
            print(i)

        return response.json()

    # 删除指定IP资产
    def delete_asset_by_address(self, address):
        """
        通过IP删除资产
        :param jms_url: JMS的URL
        :param token: 认证token
        :param address: 资产IP地址
        :return: 返回删除操作的结果
        """
        url = self.base_url + "/api/v1/assets/assets/"
 
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            assets = response.json()
            for asset in assets:
                if asset.get("address") == address:
                    asset_id = asset.get("id")
                    delete_url = self.base_url + f"/api/v1/assets/assets/{asset_id}/"
                    delete_response = requests.delete(delete_url, headers=self.headers)
                    if delete_response.status_code == 204:
                        print(f"成功删除IP为 {address} 的资产！")
                        return '删除成功'
                    else:
                        print(f"删除IP为 {address} 的资产失败！")
                        return '删除失败'
            print(f"找不到IP为 {address} 的资产！")
            return '找不到资产'
        else:
            print("获取资产列表失败！")
            print(response.json())
            return '获取资产列表失败!'


if __name__ == '__main__':
    pass
