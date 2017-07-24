# -*- coding:utf-8 -*-
import os
import sys
import shutil

from run import login, logout, get_name_list
from base import clear, store_data, DATA, EXCEPTIONS, POSTDATA, PATH, LOG, STATUS


def init(success=True):
    '初始化几个文件'
    if success:
        with open('success.txt', 'w+'):
            pass
    with open('retry.txt', 'w+'):
        pass
    with open('error.txt', 'w+'):
        pass
    with open('fail.txt', 'w+'):
        pass


def pause():
    '见名知意'
    input('按任意键继续\n')


def file_print(content, file_name=sys.stdout, model=0):
    '文件输出'
    if not os.path.exists(file_name):
        with open(file_name, 'w+'):
            pass
    if model == 0:
        print(content)
    elif model == 1:
        out = open(file_name, 'a+')
        print(content, file=out)
        out.close()
    elif model == 2:
        out = open(file_name, 'a+')
        print(content)
        print(content, file=out)
        out.close()


def test_name(name):
    '测试某个用户'
    login(name)
    if DATA['result'] == 'success' and not DATA['maxFlow']:
        DATA['result'] = 'retry'
    content = "%s\t%s\t%s" % (name, DATA['result'], DATA['maxFlow'])
    file = DATA['result'] + '.txt'
    file_print(content, file, 2)
    logout(POSTDATA)


def test_file(file):
    '对某个文件进行测试'
    name_list = get_name_list(file)
    if STATUS.UPDATE:
        if not STATUS.UPDATE_ALL:
            STATUS.UPDATE_ALL = len(name_list)
            STATUS.UPDATE_NOW = 0
        else:
            STATUS.UPDATE_ALL += len(name_list)
    for name in name_list:
        if file != 'NameList.txt':
            name = name.split('\t')[0]
        test_name(name)
        clear(DATA)
        STATUS.UPDATE_NOW += 1


def choose(num, out_label):
    '筛选'
    file_name = 'result/%dMB.%s.txt' % (num, out_label)
    if os.path.isfile(file_name):
        with open(file_name, 'w+'):
            pass
    if not os.path.exists('result'):
        os.mkdir('result')
    if os.path.isfile('success.txt'):
        if os.path.getsize('success.txt'):
            name_list = get_name_list('success.txt')
        else:
            print('所有账号都没有流量了, GG')
            return
    else:
        print('文件"success.txt"不存在, 请重新进行测试')
        raise FileExistsError
    try:
        for name in name_list:
            each = name.split('\t')
            if len(each) > 1:
                flow = float(each[2].replace('MB', ''))
                if flow > num:
                    file_print(each[0], file_name, 1)
        return file_name
    except EXCEPTIONS as error:
        LOG.error(error)
        LOG.error('文件"success.txt"异常')
        return


def update(out_label='fast'):
    os.chdir(os.path.join(PATH, 'src'))
    try:
        init()
        if out_label == 'fast':
            test_file('FastNameList.txt')

        elif out_label == 'full':
            test_file('AllNameList.txt')

        test_file('error.txt')
        test_file('retry.txt')
    except EXCEPTIONS as error:
        LOG.error(error)
        return

    success_file = 'result/success.%s.txt' % (out_label)
    file_name = choose(0, out_label)

    if os.path.isfile('error.txt'):
        os.remove('error.txt')
    if os.path.isfile('retry.txt'):
        os.remove('retry.txt')
    if os.path.isfile('fail.txt'):
        os.remove('fail.txt')
    if os.path.isfile('NameList.txt'):
        with open('NameList.txt', 'w+'):
            pass

    if file_name:
        shutil.copy('success.txt', success_file)
        shutil.copy(file_name, 'NameList.txt')
        os.remove(file_name)
        os.remove(success_file)

    STATUS.UPDATE = None
    STATUS.UPDATE_ALL = 0
    STATUS.UPDATE_NOW = 0


def main():
    '主函数'
    os.chdir(os.path.join(PATH, 'src'))

    try:
        print('是否跳过流量测试?')
        print('一般在你最近已经测试过, 且在该文件夹下有一个非空的名为"success.txt"的文件时选择跳过')
        print('完整测试时间可能较久,请耐心等待')
        user_input = input('按0快速测试, 按1完整测试, 按任意其他键跳过测试\n')
        if str(user_input) == '0':
            init()
            test_file('FastNameList.txt')
            out_label = 'fast'
        elif str(user_input) == '1':
            init()
            test_file('AllNameList.txt')
            out_label = 'full'
        else:
            init(success=False)
            out_label = 'pass'

        test_file('error.txt')
        test_file('retry.txt')
    except EXCEPTIONS as error:
        LOG.error(error)
        sys.exit()

    success_file = 'result/success.%s.txt' % (out_label)
    print('测试完毕, 想要筛选剩余流量大于多少MB的账号?')
    print('例如: 想找剩余流量大于10000MB的, 就输入10000, 按回车即可')
    try:
        num = int(input('清输入一个整数, 按回车确认, 不要输入任何其他字符\n'))
    except EXCEPTIONS:
        print('输入错误, 默认筛选0')
        num = 0

    file_name = choose(num, out_label)
    if not file_name:
        sys.exit()
    print('筛选完毕')

    if os.path.isfile('error.txt'):
        os.remove('error.txt')
    if os.path.isfile('retry.txt'):
        os.remove('retry.txt')
    if os.path.isfile('fail.txt'):
        os.remove('fail.txt')
    if os.path.isfile('NameList.txt'):
        with open('NameList.txt', 'w+'):
            pass

    shutil.copy('success.txt', success_file)
    shutil.copy(file_name, 'NameList.txt')
    os.remove(file_name)
    os.remove(success_file)

    print('更新完毕')
    input('按任意键退出')


if __name__ == '__main__':
    main()
