import os
import sys
import shutil

from run import login, logout, get_name_list, log
from base import clear, DATA, EXCEPTIONS, POSTDATA, PATH

def init():
    '初始化几个文件'
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

def file_print(content, file=sys.stdout, model=0):
    '文件输出'
    if model == 0:
        print(content)
    elif model == 1:
        out = open(file, 'a+')
        print(content, file=out)
        out.close()
    elif model == 2:
        out = open(file, 'a+')
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
    for name in get_name_list(file):
        if file != 'NameList.txt':
            name = name.split('\t')[0]
        test_name(name)
        clear(DATA)

def choose(num):
    '筛选'
    file_name = 'result/大于%dMB.txt' % num
    if not os.path.exists('result'):
        os.mkdir('result')
    if os.path.isfile('success.txt') and os.path.getsize('success.txt'):
        name_list = get_name_list('success.txt')
    else:
        log.error('文件"success.txt"不存在或为空, 请重新打开程序进行测试')
        sys.exit()
    try:
        for name in name_list:
            each = name.split('\t')
            if len(each) > 1:
                flow = float(each[2].replace('MB', ''))
                if flow > num:
                    file_print(each[0], file_name, 1)
        return file_name
    except EXCEPTIONS as error:
        log.error(error)
        log.error('文件"success.txt"异常')
        sys.exit()

def main():
    '主函数'
    os.chdir(os.path.join(PATH, 'src'))

    try:
        print('是否跳过流量测试?')
        print('一般在你最近已经测试过, 且在该文件夹下有一个非空的名为"success.txt"的文件时选择跳过')
        print('完整测试时间可能较久,请耐心等待')
        if str(input('按1跳过测试, 按任意其他键继续测试\n')) != '1':
            init()
            test_file('OriginalNameList.txt')
            test_file('error.txt')
            test_file('retry.txt')
    except EXCEPTIONS as error:
        log.error(error)
        sys.exit()

    print('测试完毕, 想要筛选剩余流量大于多少MB的账号?')
    print('例如: 想找剩余流量大于10000MB的, 就输入10000, 按回车即可')
    try:
        num = int(input('清输入一个整数, 按回车确认, 不要输入任何其他字符\n'))
    except EXCEPTIONS:
        print('输入错误, 请重新运行程序(选择跳过测试)')
        sys.exit()

    file_name = choose(num)
    print('筛选完毕')

    # if str(input('按1清理生成的临时文件, 按任意其他键跳过\n')) is '1':
    if os.path.isfile('error.txt'):
        os.remove('error.txt')
    if os.path.isfile('retry.txt'):
        os.remove('retry.txt')
    if os.path.isfile('fail.txt'):
        os.remove('fail.txt')
    if os.path.isfile('NameList.txt'):
        os.remove('NameList.txt')
    shutil.copy(file_name, 'NameList.txt')
    print('更新完毕')
    input('按任意键退出')

if __name__ == '__main__':
    main()

