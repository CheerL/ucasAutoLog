import subprocess
import sys
import os
import time

def getPath():
    try:
        if os.path.isfile('C:\\config') is True:
            file = open('C:\\config','r')
            Path = file.readline()
            file.close()
        else:
            raise Exception()
    except:
        os.system('echo Error.&echo 请重新运行安装程序"install.exe".&pause')
        sys.exit()
    return Path

Path = getPath()
os.chdir(Path)
while True:
    try:
        try:
            if os.path.isfile('main.exe') is True:
                autoLogin = subprocess.Popen('main.exe')
            else:
                raise Exception()
        except:
            os.system('echo Error.&echo 请检查文件完整性.')
            sys.exit()
        autoLogin.wait()
        time.sleep(5)
    except:
        autoLogin.kill()
        os.system('echo Error.&echo 请重新运行"autoLogin.exe".')
        os.system('关闭程序.bat')
        sys.exit()
        
        
    
    
