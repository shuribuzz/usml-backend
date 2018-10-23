import pika
import sys
import json
import syslog


class ConsumeMail:
    def start_consume_mail(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

            channel = connection.channel()
            channel.queue_declare(queue='queue_mail', durable=True)
            channel.basic_consume(self.callback_mail,
                                  queue='queue_mail',
                                  no_ack=True)

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog("Error while consuming queue mail: %s" % str(exc))

        connection.close()
        sys.exit(1)

    def callback_mail(self, ch, method, properties, body):
        # будем отправлять подтверждение из обработчика сразу после выполнения задачи
        if self.callback_body(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def callback_body(self, body):
        self.send_mail(body)

    def send_mail(self, body_msg):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.header import Header
        from validate_email import validate_email

        try:
            my_mail = 'mail@mail.server'
            mailDict = json.loads(body_msg)
            mail_is_valid = validate_email(mailDict['mail'])

            if mail_is_valid is not True:
                raise Exception("invalid e-mail: " + mailDict['mail'])

            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(mailDict['subject'], 'utf-8')
            msg['From'] = my_mail
            msg['To'] = mailDict['mail']

            msgText = MIMEText(mailDict['message'].encode(
                'utf-8'), 'plain', 'utf-8')
            msg.attach(msgText)

            s = smtplib.SMTP('mail.server')
            s.sendmail(my_mail, mailDict['mail'], msg.as_string())
            syslog.syslog("Sending email-massage to: %s" % (mailDict['mail']))
            if s:
                s.quit()
                return True
        except Exception as exc:
            syslog.syslog("Error while sending e-mail: %s" % (exc))
            s.quit()
            return False
