import os
import sys
import time
import subprocess
import platform

def isfile(filename):
    return os.path.isfile(filename)

def hideFile(path,model=True):
    if 'Windows' in platform.system():
        if model is True:
            cmd = os.popen('attrib +h "' + path +'"')
        if model is False:
            cmd = os.popen('attrib -h "' + path +'"')
        cmd.close()
        time.sleep(1)
def setVersion(ver):
    if os.path.isfile('config') is True:
        hideFile('config',False)
    config = open('config','w+')
    config.write(ver)
    config.close()
    hideFile('config',True)

print('开始安装.\n')

print('--------------------\n\nStep 1\n检测文件完整性.\n')
FileList = {'uninstall.bat','main.exe','src\\NameList.txt',
            'autoLogin.exe','设置自动启动.bat','清理日志.bat','关闭程序.bat',
            'src\\OriginalNameList.txt','listUpdate.exe'}
for each in FileList:
    if isfile(each) is False:
        os.system("echo 安装失败.&echo 文件 "+each+" 缺失.&pause")
        sys.exit()
time.sleep(1)
print('Success.\n\n--------------------\n')

time.sleep(1)
print('Step 2\n设置运行路径.\n')

try:
    if os.path.isfile('C:\\config'):
        os.remove('C:\\config')
    file = open('C:\\config','w+')
    file.write(os.getcwd())
    file.close()
    hideFile('C:\\config',True)
except:
    os.system("echo Error.&echo 请尝试以管理员身份运行.&pause")
    sys.exit()
    
time.sleep(1)
print('Success.\n\n--------------------\n')

time.sleep(1)
print('Step 3\n设置自动启动.\n')
os.system('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "autoLogin" /t reg_sz /d "%cd%\autoLogin.exe" /f>nul')
print('Success.\n\n--------------------\n')

time.sleep(1)
os.system('cls')
print('安装成功.\n如果想移动该程序,\n请将整个文件夹一起移动,\n并重新运行安装程序.\n')

setVersion('130')

time.sleep(1)
print('\n自动执行程序"autoLogin.exe"\n10秒后程序自动关闭.')
subprocess.Popen('autoLogin.exe')
time.sleep(10)
sys.exit()
