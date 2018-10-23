import pika
import sys
import json
import syslog


class ConsumeSMS:
    def start_consume_sms(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

            channel = connection.channel()
            channel.queue_declare(queue='queue_sms', durable=True)
            channel.basic_consume(self.callback_sms,
                                  queue='queue_sms',
                                  no_ack=True
                                  )

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue sms: %s" % str(exc))
        connection.close()
        sys.exit(1)

    def callback_sms(self, ch, method, properties, body):
        # будем отправлять подтверждение из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
        self.send_sms(body)

    def send_sms(self, body_sms):
        print('4')
        smsDict = json.loads(body_sms)

        number = smsDict['number']
        subject = smsDict['subject']
        message = smsDict['message']

        message = subject + " " + message
        message = message.replace('\n', '')
        message = message[:70].encode('utf-8')

        try:
            connection = dbModule.Connection("db_login/db_pass")
            cursor = connection.cursor()

            sql = "DECLARE res_v VARCHAR (100); \
            BEGIN send_procedure(%s, %s); COMMIT; END;" \
                  % (number.encode('utf-8'), message)

            cursor.execute(sql)

            syslog.syslog("Sending SMS message to: %s" % (smsDict['number']))
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            return True
        except Exception as exc:
            syslog.syslog("Error while sending SMS notification: %s" % (exc))
            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
