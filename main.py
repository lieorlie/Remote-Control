from test.SendEmail import SendEmail
from test.GetEmail import GetEmail
from test.Command import Command
import time

if __name__ == '__main__':
    # testSend = SendEmail()
    testGet = GetEmail()

    while True:
        testGet.Get()

        if testGet.flag:
            print("读取邮件内容成功，内容如下")
            print(testGet.dic)
            cmd = Command(testGet.dic)
            cmd.Run()
            testGet.Restart() #成功读取命令邮件名进行操作后，重新将flag置为0，让程序继续

        else:
            print("正在读取的邮件不是命令邮件")


        time.sleep(3)


