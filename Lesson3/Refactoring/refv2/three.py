import pika
import sys
import json
import syslog

class ConsumeThree:
    def start_consume_three(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

            channel = connection.channel()
            channel.queue_declare(queue='queue_three', durable=True)
            # Подтверждение (ack) отправляется подписчиком для информирования RabbitMQ о том,
            # что полученное сообщение было обработано и RabbitMQ может его удалить.
            channel.basic_consume(self.callback_three,
                                  queue='queue_three',
                                  no_ack=False)

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue three: %s" % str(exc))

        connection.close()
        sys.exit(1)


    '''Сообщение будет заново передано только тогда, когда программа-обработчик будет остановлена,
       но RabbitMQ будет потреблять все больше и больше памяти, т.к. не будет удалять неподтвержденные
       сообщения.
    '''
    def callback_three(self, ch, method, properties, body):
        # будем отправлять подтверждение из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
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
