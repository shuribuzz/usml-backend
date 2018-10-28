import json
import syslog


class ConsumeMail:
    def __init__(self, body):
        self.body = body

    def notify_mail(self, body):
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
