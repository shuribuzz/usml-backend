import json
import syslog
import telegram

class ConsumeTelegram:
    def __init__(self, body):
        self.body = body
        self.params = {"telegram": {"token": "id:token",
                               "base_url": "https://api.telegram.org/bot",
                               'proxy': {
                                   'ip': '0.0.0.0',
                                   'port': 9999, 'user': 'some_user', 'password': 'some_password'}},
                  "to_db": {'url_in': 'some url in'}}


    def notify_telegram(self, body):
        syslog.syslog("%s: send data to telegramm %s" % (self.queue, body))
        params = self.params["telegram"]
        t = telegram_api(params["token"], proxy=params.get('proxy'))
        data = json.loads(body)
        chat_id = data["chat_id"]
        mess = data["message"]
        return t.send(chat_id, mess) or True


class telegram_api:
    def __init__(self, token, proxy={}):
        self.BOT_TOKEN = token
        self.cmd = {"stat": "getMe", "send": "sendMessage"}
        if proxy:
            ip = proxy['ip']
            port = proxy['port']
            user = proxy['user']
            passwd = proxy['password']
            pp = telegram.utils.request.Request(proxy_url='socks5://%s:%s' % (
                ip, port), urllib3_proxy_kwargs={'username': user, 'password': passwd})
        else:
            pp = telegram.utils.request.Request()
        self.bot = telegram.Bot(token=self.BOT_TOKEN, request=pp)

    def stat(self):
        # cmd=self.cmd["stat"]
        try:
            pass
        except Exception as err:
            messToSyslog = "Fail to read telegram_bot status: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)

    def send(self, chat, mess):
        # cmd = self.cmd["send"]
        mess = mess.encode('utf-8')
        try:
            self.bot.sendMessage(chat, mess)
            return True
        except Exception as err:
            messToSyslog = "Fail to sendmessage via telegram_bot: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)