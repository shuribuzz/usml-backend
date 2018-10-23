import pika
import sys
import json
import syslog
import telegram_api


class ConsumeHTlgrmOne:
    def start_consume(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                host='localhost'))

            channel = connection.channel()

            channel.queue_declare(queue='queue_Tgm_1', durable=True)
            channel.basic_consume(self.callback,
                                  queue='queue_Tgm_1',
                                  no_ack=False, exclusive=False)
            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue Telegram: %s" % str(exc))
        connection.close()
        sys.exit(1)

        connection.close()

    def callback(self, ch, method, properties, body):
        # будем отправлять подтверждение из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
        self.telegram(body)

    def telegram(self, body):
        syslog.syslog("queue_Tgm_1 send data to telegramm %s" % (body))
        params = self.params["telegram"]
        t = telegram_api(params["token"], proxy=params.get('proxy'))
        data = json.loads(body)
        chat_id = data["chat_id"]
        mess = data["message"]
        return t.send(chat_id, mess) or True
