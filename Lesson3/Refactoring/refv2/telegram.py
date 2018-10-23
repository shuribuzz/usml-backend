import pika
import sys
import json
import syslog
import telegram


class ConsumeTelegram:
    def start_consume_telegram(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

            channel = connection.channel()
            channel.queue_declare(queue='queue_tlgrm', durable=True)
            channel.basic_consume(self.callback_telegram,
                                  queue='queue_tlgrm',
                                  no_ack=True
                                  )

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue tlgrm: %s" % str(exc))

        connection.close()
        sys.exit(1)

    def callback_telegram(self, ch, method, properties, body):
        # будем отправлять подтверждение из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
        self.send_telegram(body)

    def send_telegram(self, body_telegram):
        try:
            # Telegram Bot
            pp = telegram.utils.request.Request(proxy_url='socks5://0.0.0.0:9999', urllib3_proxy_kwargs={
                'username': 'some_username', 'password': 'some_password'})
            bot = telegram.Bot(
                token='id:token', request=pp)

            telegramData = json.loads(body_telegram)
            bot.sendMessage(telegramData['channel'], telegramData['message'])
            return True
        except Exception as exc:
            syslog.syslog("Error while sending telegram: %s" % (exc))
            return False
