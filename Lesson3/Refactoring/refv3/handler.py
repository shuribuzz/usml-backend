import pika
import sys
import syslog
from consume_one import ConsumeOne
from consume_two import ConsumeTwo
from consume_three import ConsumeThree
from consume_mail import ConsumeMail
from consume_sms import ConsumeSMS
from consume_telegram import ConsumeTelegram
from consume_psevdotelegram import ConsumePsevdotelegram



class Handler:
    def __init__(self, queue):
        self.queue = queue

        if queue == "queue_one":
            self.notify = self.one
        elif queue == "queue_two":
            self.notify = self.two
        elif queue == "queue_three":
            self.notify = self.three
        elif queue == "queue_mail":
            self.notify = self.mail
        elif queue == "queue_sms":
            self.notify = self.sms
        elif queue == "queue_tlgrm":
            self.notify = self.telegram
        elif queue == "queue_Tgm_1":
            self.notify = self.psevdotelegram
        else:
            self.notify = self.default


    def start_consume(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_consume(self.callback,
                                  queue=self.queue,
                                  no_ack=False, exclusive=False)
            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            # channel.stop_consuming()
            syslog.syslog("Error while consuming %s queue: %s" %
                          (self.queue, str(exc)))
        connection.close()
        sys.exit(1)

        connection.close()

    def callback(self, ch, method, properties, body):
        if self.notify(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def one(self, body):
        ConsumeOne().notify_one(body)

    def two(self, body):
        ConsumeTwo().notify_two(body)

    def three(self, body):
        ConsumeThree().notify_three(body)

    def mail(self, body):
        ConsumeMail().notify_mail(body)

    def sms(self, body):
        ConsumeSMS().notify_sms(body)

    def telegram(self, body):
        ConsumeTelegram().notify_telegram(body)

    def psevdotelegram(self, body):
        ConsumePsevdotelegram().notify_psevdotelegram(body)

    def default(self, body):
        messToSyslog = "got " + body + " but not set notifyer"
        syslog.syslog("%s: %s" % (self.queue, messToSyslog))
        return True
