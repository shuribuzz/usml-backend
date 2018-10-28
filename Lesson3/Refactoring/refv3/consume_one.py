import json
import syslog
import re
import requests

class ConsumeOne:
    def __init__(self, body):
        self.body = body

    def notify_one(self, body):
        row = self.create_one(body)
        db_result = self.db_process_one(row)
        result = self.event_update_one(db_result)
        return result

    def create_one(self, body_msg):
        tt = json.loads(body_msg)

        try:
            row = [
                tt['hostname'].encode('utf-8'),
                tt['hostname'].encode('utf-8'),
                tt['state-trigger'].encode('utf-8'),
                "Автоматически создано \nevent: " +
                str(tt['event'].encode('utf-8')),
                tt['check-type'].encode('utf-8'),
                int(tt['trigger']),
                tt['message'].encode('utf-8'),
                tt.get('zhost', 'some.host').encode('utf-8')
            ]

            syslog.syslog('Message: {} {} {}'.format(tt['hostname'].encode(
                'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % exc)
            return False

    def db_process_one(self, row):
        if not row:
            return False
        zhost = row[7]

        try:
            connection = dbModule.Connection("db_login/db_pass")
        except dbModule.DatabaseError as exc:
            syslog.syslog("DB connection error: %s" % exc)
            return False

        try:
            cursor = connection.cursor()
            statTT = cursor.var(dbModule.STRING, 255)
            result = cursor.var(dbModule.NUMBER, 255)
            numTT = cursor.var(dbModule.NUMBER, 255)
            cursor.prepare("""BEGIN;
                procedure_one(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);
            ); END;""")
            row.append(result)
            row.append(numTT)
            row.append(statTT)
            cursor.execute(None, row)
            connection.commit()
            cursor.close()
            syslog.syslog("Insert data to db: %s" % row[0])
        except Exception as exc:
            syslog.syslog("Error while inserting to db: %s" % exc)
            return False

        event_num = re.search("\s*([0-9]+)", row[6]).group(1)
        resultTT = (int(row[-3].getvalue()),
                    int(row[-2].getvalue()), str(row[-1].getvalue()))

        syslog.syslog("Prepare ack one: %s" % row)
        return (zhost, event_num, resultTT)

    def event_update_one(self, data):
        if not data:
            return False
        zhost, evid, NumTT = data

        server = 'server'
        if zhost == 'server2':
            server = 'server2'

        login = 'event_login'
        password = 'event_password'

        s = requests.Session()
        s.auth = (login, password)

        return True
