import requests
import json
from digigru.local_settings import CONOHA_IDENTITY_SERVER_URL, CONOHA_API_USERNAME, CONOHA_API_PASSWORD, CONOHA_OBJECT_STRAGE_SERVER_URL, CONOHA_TENANT_ID


def getToken():
    """
    tokenの取得
    :param userName:
    :param password:
    :param tenantId:
    :param url:
    :return:
    """
    headers = {
        'Accept': 'application/json',
    }
    data = '{"auth":{"passwordCredentials":{"username":"%s","password":"%s"},"tenantId":"%s"}}' % (
        CONOHA_API_USERNAME, CONOHA_API_PASSWORD, CONOHA_TENANT_ID)
    response = requests.post(CONOHA_IDENTITY_SERVER_URL,
                             headers=headers, data=data)
    data = response.json()
    return data["access"]["token"]["id"]


def uploadObject(path, container, fileName):
    """
    オブジェクトのアップロード
    :param token:
    :param path:
    :param objectStorageUrl:
    :param container:
    :param fileName:
    :return:
    """
    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': getToken(),
    }
    with open(path, 'rb') as file:
        response = requests.put(
            CONOHA_OBJECT_STRAGE_SERVER_URL + '/' + container + '/' + fileName, headers=headers, data=file)
    return response
