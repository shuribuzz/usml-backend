import pika
import sys
import json
import syslog
import corporateDB


class ConsumeHTlgrmTwo:
    def start_consume(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='queue_tlgrm', durable=True)
            channel.basic_consume(self.callback,
                                  queue='queue_tlgrm',
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
        self.psevdo_telegram(body)

    def psevdo_telegram(self, body):
        params = self.params["to_db"]
        db = corporateDB(params['url_in'])
        data = json.loads(body)
        res, mess = db.telegram_procedure_exec(
            data['group'], data['message'])
        syslog.syslog("queue_tlgrm send data for telegramm notification %s with status %s" % (body, res))
        return True
