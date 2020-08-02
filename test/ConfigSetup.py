import configparser

#Reader类用来读取信息，并将读取出来的信息赋值给指定变量
class Reader:
    def __init__(self):
        self.reader = configparser.ConfigParser()
        self.reader.read("_config.ini", encoding="utf-8")

    def GetInfo(self, Option, Key):
        try:
            info = self.reader.get(Option, Key)
            return info
        except Exception as e:
            print(e)

    def GetOptions(self):
        try:
            options = self.reader.sections()
            return options
        except Exception as e:
            print(e)

    def GetKey(self,option):
        try:
            keys = self.reader.options(option)
            return keys
        except Exception as e:
            print(e)




