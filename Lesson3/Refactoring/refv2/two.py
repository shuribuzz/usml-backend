import pika
import sys
import json
import syslog
import re
import requests


class ConsumeTwo:
    def start_consume_two(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )
            channel = connection.channel()
            channel.queue_declare(queue='queue_two', durable=True)
            # Подтверждение (ack) отправляется подписчиком для информирования RabbitMQ о том,
            # что полученное сообщение было обработано и RabbitMQ может его удалить.
            channel.basic_consume(self.callback_two,
                                  queue='queue_two',
                                  no_ack=False)

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue two: %s" % str(exc))

        connection.close()
        sys.exit(1)


    '''Сообщение будет заново передано только тогда, когда программа-обработчик будет остановлена,
       но RabbitMQ будет потреблять все больше и больше памяти, т.к. не будет удалять неподтвержденные
       сообщения.
    '''
    def callback_two(self, ch, method, properties, body):
        # будем отправлять подтверждение(basic_ack) из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
        row = self.create_two(body)
        db_result = self.db_process_two(row)
        result = self.event_update_two(db_result)
        return result


    def create_two(self, body_msg):
        tt = json.loads(body_msg)
        try:
            row = [
                tt['hostname'].encode('utf-8'),
                tt['ip-address'].encode('utf-8'),
                tt['state-trigger'].encode('utf-8'),
                tt['message'].encode('utf-8'),
                tt['comment'].encode('utf-8'),
                tt['trigger'].encode('utf-8'),
                "Автоматически создано " +
                tt['prefix'].encode('utf-8') + "\nevent: " +
                tt['event'].encode('utf-8'),
                tt.get('zhost', 'some.host').encode('utf-8')
            ]

            syslog.syslog('Message: {} {} {}'.format(tt['hostname'].encode(
                'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % exc)
            return False

    def db_process_two(self, row):
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
            cursor.prepare("""BEGIN
            procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);
            END;""")
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

        syslog.syslog(str(row))
        event_num = re.search("\s*([0-9]+)", row[3]).group(1)
        event_reg_num = row[-2].getvalue()
        if event_reg_num == None:
            event_reg_num = 0
        event_reg_status = str(row[-1].getvalue())
        resultTT = (int(event_reg_num), event_reg_status)
        syslog.syslog("Prepare ack two: %s" % row)
        return (zhost, event_num, resultTT)

    def event_update_two(self, data):
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
