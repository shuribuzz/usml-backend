import json
import syslog

class ConsumeThree:
    def __init__(self, body):
        self.body = body

    def notify_three(self, body):
        row = self.create_three(body)
        db_result = self.db_process_three(row)
        return db_result

    def create_three(self, body_msg):
        tt = json.loads(body_msg)
        try:
            row = [tt['hostname'].encode(
                'utf-8'), tt['state-trigger'].encode('utf-8'), tt['trigger'].encode('utf-8')]

            syslog.syslog('Three message: {} {} {}'.format(tt['hostname'].encode(
                'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % (exc))
            return False

    def db_process_three(self,row):
        if not row:
            return False
        try:
            connection = dbModule.Connection("db_login/db_pass")
        except dbModule.DatabaseError as exc:
            syslog.syslog("DB connection error: %s" % exc)
            return False

        try:
            cursor = connection.cursor()
            cursor.prepare("""BEGIN;
                procedure_three(:1, :2, :3);
                END;""")
            cursor.execute(None, row)
            connection.commit()
            syslog.syslog("Insert data to db: %s" % row[0])
        except Exception as exc:
            syslog.syslog("Error while inserting to db: %s" % exc)
            return False

        return True
