import os
import sys
import time
import random
import requests
from base import POSTDATA_LOGIN, POSTDATA, PATH, DATA, HEADERS, LOG_PATH, BASE_URL, TIME_OUT, EXCEPTIONS
from base import get_logger, clear

log = get_logger('auto_login', LOG_PATH)

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

def get_name_list(filename):
    '从文件获取所有可登陆用户列表'
    try:
        with open(filename, 'r') as file:
            name_list = file.read().split('\n')[:-1]
            log.info('成功获取列表')
            return name_list
    except EXCEPTIONS as error:
        log.error(error)
        log.error('文件"%s"缺失' % filename)
        sys.exit()

def login(userId):
    '登录'
    try:
        url = BASE_URL + 'login'
        POSTDATA_LOGIN['userId'] = userId
        response = requests.post(
            url=url, data=POSTDATA_LOGIN, timeout=TIME_OUT, headers=HEADERS).json()
        DATA['result'] = response.get('result')
        if DATA['result'] == 'success':
            DATA['userIndex'] = response.get('userIndex')
            for _ in range(5):
                if test_online(DATA['userIndex']) is ONLINE:
                    break
            else:
                logout(POSTDATA)
                return LOGIN_FAIL

            log.info("目前登陆用户为:%s, 剩余流量:%s" % (DATA['userName'], DATA['maxFlow']))
            return LOGIN_SUCCESS
        else:
            return LOGIN_FAIL
    except EXCEPTIONS as error:
        DATA['result'] = 'error'
        log.error(error)
        log.error('登陆失败')
        return LOGIN_FAIL

def logout(postData):
    '退出'
    try:
        url = BASE_URL + 'logout'
        postData['userIndex'] = DATA['userIndex']
        requests.post(url=url, data=POSTDATA, timeout=TIME_OUT, headers=HEADERS)
        if not DATA['userName']:
            log.info('没有用户在线')
            return LOGOUT_FAIL
        else:
            log.info('%s下线' % DATA['userName'])
        return LOGOUT_SUCCESS
    except EXCEPTIONS as error:
        log.error(error)
        log.error('未正常离线')
        return LOGOUT_FAIL

def keep_alive(userIndex):
    '保活'
    try:
        url = BASE_URL + 'keepalive'
        POSTDATA['userIndex'] = userIndex
        if requests.post(url=url, data=POSTDATA, timeout=TIME_OUT, headers=HEADERS)\
            .json().get('result') == "success":
            return KEEP_ALIVE_SUCCESS
        else:
            raise NotImplementedError()
    except EXCEPTIONS as error:
        log.error(error)
        log.error('保活失败')
        logout(POSTDATA)
        return KEEP_ALIVE_FAIL

def test_online(userIndex):
    '测试是否在线'
    if not userIndex:
        log.info('用户不存在')
        return NO_USER

    try:
        url = BASE_URL + 'getOnlineUserInfo'
        POSTDATA['userIndex'] = userIndex
        response = requests.get(url=url, headers=HEADERS, timeout=TIME_OUT).json()
        result = response.get('result')
        if  result == 'success':
            for key, _ in DATA.items():
                DATA[key] = response.get(key)
            return ONLINE
        elif result == 'wait':
            return WAIT
        else:
            return OFFLINE
    except EXCEPTIONS as error:
        log.error(error)
        log.error('网络连接异常')
        return NET_ERROR

def net_error_react(userIndex):
    '网络异常时的操作'
    count = 0
    while test_online(userIndex) is NET_ERROR:
        if count < 3:
            log.info('网络连接已断开,请检查网线或wifi是否正常')
            time.sleep(5)
            count += 1
        elif 3 <= count < 5:
            log.info('还不行？ 拔了网线再插试试？ 关了wifi再开试试')
            time.sleep(5)
            count += 1
        else:
            log.info('程序暂时停止运行,一分钟后重新测试, 或者你可以重开该程序试试')
            log.info('若反复出现该状况,可能是学校网崩了╮(╯▽╰)╭')
            log.error('网络连接异常, 重试已达最大次数, 程序挂起')
            time.sleep(60)
            log.info('重新尝试连接')
            continue
    log.info('物理连接恢复')

def main():
    '主函数'
    log.info('自动登陆程序开始运行')
    os.chdir(PATH)
    name_list = get_name_list('src/NameList.txt')

    while name_list:
        # time.sleep(10)
        test_result = test_online(DATA['userIndex'])
        if test_result is ONLINE or test_result is WAIT:
            keep_alive(DATA['userIndex'])
        elif test_result is NET_ERROR:
            net_error_react(DATA['userIndex'])
        elif test_result is NO_USER:
            name = random.choice(name_list)
            login(name)
        elif test_result is OFFLINE:
            for _ in range(10):
                if test_online(DATA['userIndex']) is ONLINE:
                    break
            else:
                if DATA['userIndex']:
                    log.error('连接错误,等待重连')
                    logout(POSTDATA)
                    clear(DATA)
                if login(name) is LOGIN_FAIL:
                    name_list.remove(name)
                    name = random.choice(name_list)
                    log.info('切换用户')

if __name__ == '__main__':
    main()
