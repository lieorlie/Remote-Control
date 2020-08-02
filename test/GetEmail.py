from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import os
from test.ConfigSetup import Reader

#GetEmail类用来读取邮件内容以及解析其内容
class GetEmail:

    def __init__(self):
        self.flag = 0 #flag为0说明没有接收到command
        self.reader = Reader()
        self.EmailHost = self.reader.GetInfo("GetEmailInfo", "EmailHost")  # 设置pop3服务器
        self.EmailUser = self.reader.GetInfo("GetEmailInfo", "EmailUser")  # 读取邮件的邮箱地址
        self.EmailCode = self.reader.GetInfo("GetEmailInfo", "EmailCode")  # 第三方客户端登录需要的口令

    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # decode_str方法的作用是将传进来的未解码的字符串进行解码
    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        # print('.....value:{0}, charset:{1}......'.format(value, charset))
        if charset:
            value = value.decode(charset)  # vlaue即字符串的值，charset是其编码方式
        return value

    def print_info(self, msg, indent=0):

        if indent == 0:
            self.dic = {}
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                # print(value)
                if value:
                    if header == 'Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                self.dic[header] = value
                # print('%s%s: %s' % ('  ' * indent, header, value))

        if (msg.is_multipart()):
            parts = msg.get_payload()
            self.print_info(parts[0], indent + 1)

        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                # print('%sText: %s' % ('  ' * indent, content + '...'))
                if indent == 1:
                    content = content.split('--')[0].replace('\n', '').strip(' ')

                self.dic["Content"] = content
                # return content
            else:
                print('%sAttachment: %s' % ('  ' * indent, content_type))

            if self.dic['Subject'] == 'command':
                self.flag = 1  # 接收到命令邮件的指令，将flag置为1说明该邮件为命令邮件

    def Get(self):

        pop = poplib.POP3_SSL(self.EmailHost)
        pop.user(self.EmailUser)
        pop.pass_(self.EmailCode)
        resp, Emails, octets = pop.list()
        index = len(Emails) #最新一封邮件的索引号
        resp, email, octets = pop.retr(index)
        msg_content = b'\r\n'.join(email).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        self.print_info(msg)
        if self.flag:
            pop.dele(index) #如果flag为1说明命令邮件的内容已经存进了dic中，然后删除命令邮件，避免重复读取
        pop.quit()


    def Restart(self):
        self.flag = 0 #重置后flag重新赋值为0，表示可以再次接收信息