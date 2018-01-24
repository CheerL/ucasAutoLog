#! /usr/bin/python3
import os
import sys
import time
import random
import requests

from base import POSTDATA_LOGIN, POSTDATA, PATH, DATA, HEADERS, BASE_URL, TIME_OUT, EXCEPTIONS
from base import STATUS, clear
from logger import Logger

LOG = Logger('auto_login')


# 登陆常量
LOGIN_SUCCESS = 0
LOGIN_FAIL = -1
# 退出常量
LOGOUT_SUCCESS = 0
LOGOUT_FAIL = -1
# 保活常量
KEEP_ALIVE_SUCCESS = 0
KEEP_ALIVE_FAIL = -1
# 测试在线常量
ONLINE = 0
NET_ERROR = -1
NO_USER = -2
WAIT = -3
OFFLINE = -4


def status_change(_login, _user='', _flow=''):
    STATUS.LOGIN = _login
    STATUS.USER = _user
    STATUS.FLOW = _flow


def get_name_list(filename):
    '从文件获取所有可登陆用户列表'
    try:
        with open(filename, 'r') as file:
            name_list = file.read().split('\n')[:-1]
            LOG.info('成功获取列表')
            return name_list
    except EXCEPTIONS as error:
        LOG.error(error)
        LOG.error('文件"%s"缺失' % filename)
        return


def login(user_id, check=True):
    '登录'
    try:
        url = BASE_URL + 'login'
        if check:
            POSTDATA_LOGIN['userId'] = user_id
        else:
            POSTDATA_LOGIN['userId'] = '%E5%95%8A%5C' + user_id
        response = requests.post(
            url=url, data=POSTDATA_LOGIN, timeout=TIME_OUT, headers=HEADERS)
        response.encoding = 'utf-8'
        response = response.json()
        DATA['result'] = response.get('result')
        if DATA['result'] == 'success':
            DATA['userIndex'] = response.get('userIndex')
            if check:
                for _ in range(5):
                    if test_online(DATA['userIndex']) is ONLINE:
                        break
                else:
                    LOG.warning('{} 尝试登录成功但未获得返回数据, 登录失败'.format(user_id))
                    logout(POSTDATA)
                    return LOGIN_FAIL

                LOG.info("目前登陆用户为:%s, 剩余流量:%s" %
                        (DATA['userName'], DATA['maxFlow']))
                return LOGIN_SUCCESS
            else:
                LOG.info('目前登陆用户为%s' % user_id)
                return LOGIN_SUCCESS
        else:
            LOG.warning('{} 登录失败, {}'.format(user_id, response.get('message')))
            return LOGIN_FAIL
    except EXCEPTIONS as error:
        DATA['result'] = 'error'
        LOG.error(error)
        LOG.error('登陆失败')
        return LOGIN_FAIL


def logout(post_data):
    '退出'
    try:
        url = BASE_URL + 'logout'
        post_data['userIndex'] = DATA['userIndex']
        requests.post(url=url, data=POSTDATA,
                      timeout=TIME_OUT, headers=HEADERS)
        if not DATA['userName']:
            LOG.info('没有用户在线')
            return LOGOUT_FAIL
        else:
            LOG.info('%s下线' % DATA['userName'])
            return LOGOUT_SUCCESS
    except EXCEPTIONS as error:
        LOG.error(error)
        LOG.error('未正常离线')
        return LOGOUT_FAIL


def keep_alive(user_index):
    '保活'
    try:
        url = BASE_URL + 'keepalive'
        POSTDATA['userIndex'] = user_index
        response = requests.post(url=url, data=POSTDATA, timeout=TIME_OUT, headers=HEADERS).json()
        if response.get('result') == "success":
            return KEEP_ALIVE_SUCCESS
        else:
            raise NotImplementedError()
    except EXCEPTIONS as error:
        LOG.error(error)
        LOG.error('保活失败')
        logout(POSTDATA)
        return KEEP_ALIVE_FAIL


def test_online(user_index):
    '测试是否在线'
    if not user_index:
        LOG.info('没有指定user index, 用户不在线')
        status_change(False)
        return NO_USER

    try:
        url = BASE_URL + 'getOnlineUserInfo'
        POSTDATA['userIndex'] = user_index
        response = requests.get(url=url, headers=HEADERS,
                                timeout=TIME_OUT)
        response.encoding = 'utf-8'
        response = response.json()
        result = response.get('result')
        if result == 'success':
            for key, _ in DATA.items():
                DATA[key] = response.get(key)
            status_change(True, DATA['userName'], DATA['maxFlow'])
            return ONLINE
        elif result == 'wait':
            return WAIT
        else:
            status_change(False)
            return OFFLINE
    except EXCEPTIONS as error:
        LOG.error(error)
        LOG.error('网络连接异常')
        status_change(False)
        return NET_ERROR


def net_error_react(user_index):
    '网络异常时的操作'
    count = 0
    while test_online(user_index) is NET_ERROR:
        if count < 3:
            LOG.info('网络连接已断开,请检查网线或wifi是否正常')
            time.sleep(5)
            count += 1
        elif 3 <= count < 5:
            LOG.info('还不行？ 拔了网线再插试试？ 关了wifi再开试试')
            time.sleep(5)
            count += 1
        else:
            LOG.info('程序暂时停止运行,一分钟后重新测试, 或者你可以重开该程序试试')
            LOG.info('若反复出现该状况,可能是学校网崩了╮(╯▽╰)╭')
            LOG.error('网络连接异常, 重试已达最大次数, 程序挂起')
            time.sleep(10)
            LOG.info('重新尝试连接')
            continue
    LOG.info('物理连接恢复')


def main():
    '主函数'
    LOG.info('自动登陆程序开始运行')
    os.chdir(PATH)
    name_list = get_name_list('src/NameList.txt')

    while name_list:
        time.sleep(10)
        test_result = test_online(DATA['userIndex'])
        # print(test_result)
        if test_result is ONLINE or test_result is WAIT:
            pass
        elif test_result is NET_ERROR:
            net_error_react(DATA['userIndex'])
        elif test_result is NO_USER:
            name = random.choice(name_list)
            login(name, False)
        elif test_result is OFFLINE:
            for _ in range(10):
                if test_online(DATA['userIndex']) is ONLINE:
                    break
            else:
                if DATA['userIndex']:
                    LOG.error('连接错误,等待重连')
                    logout(POSTDATA)
                    clear(DATA)
                if login(name, False) is LOGIN_FAIL:
                    # if len(name_list) > 10:
                    #     name_list.remove(name)
                    name = random.choice(name_list)
                    LOG.info('切换用户')

    STATUS.RUN = False


if __name__ == '__main__':
    main()
