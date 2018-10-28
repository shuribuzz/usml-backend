import json
import syslog

class ConsumePsevdotelegram:
    def __init__(self, body):
        self.body = body
        self.params = {"telegram": {"token": "id:token",
                               "base_url": "https://api.telegram.org/bot",
                               'proxy': {
                                   'ip': '0.0.0.0',
                                   'port': 9999, 'user': 'some_user', 'password': 'some_password'}},
                  "to_db": {'url_in': 'some url in'}}

    def notify_psevdotelegram(self, body):
        params = self.params["to_db"]
        db = corporateDB(params['url_in'])
        data = json.loads(body)
        res, mess = db.telegram_procedure_exec(
            data['group'], data['message'])
        syslog.syslog("%s: send data for telegramm notification %s with status %s" % (
            self.queue, body, res))
        return True


class corporateDB:
    def __init__(self, url_in):
        self.connection = dbModule.Connection("login/password")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''BEGIN
                            some_initial_procedure(%s);
                            END;''' % url_in)

    def telegram_procedure_exec(self, group, message):
        self.cursor.execute("""BEGIN
                        another_plsql_procedure(%s);
                        COMMIT;
                        END;""" % message, group=int(group), result_out=result_out, message_out=message_out)
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return result_out.getvalue(), message_out.getvalue()