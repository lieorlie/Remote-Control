import os
import win32api
from test.ConfigSetup import Reader


class Command:
    def __init__(self, dic):
        try:
            self.From = dic['From']
            self.Content = dic['Content'].split('@')
            self.reader = Reader()
            # self.RunCmd = self.reader.GetInfo("Command", self.Cmd)

        except Exception as e:
            print(e)

    def Run(self):
        try:
            Option = self.Content[0]
            Key = self.Content[1]
            print(Option)
            print(Key)
            if self.From == ' <zmjmq123@sina.com>' and Option in self.reader.GetOptions() and Key in self.reader.GetKey(Option):

                if Option == 'Command':
                    #运行cmd命令
                    key = self.reader.GetInfo(Option, Key)
                    os.system('chcp 65001')
                    os.system(key)

                elif Option == 'Open':
                    key = self.reader.GetInfo(Option, Key)
                    win32api.ShellExecute(0, 'open', key, '', '', 1)


                elif Option == 'Box':
                    key = self.reader.GetInfo(Option, Key)
                    win32api.MessageBox(0, key, "神奇盒子")


                else:
                    print("出错!命令不存在!!!")

        except Exception as e:
            print(e)