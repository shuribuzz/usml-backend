from threading import Thread
import syslog
import time
from one import ConsumeOne
from two import ConsumeTwo
from three import ConsumeThree
from mail import ConsumeMail
from sms import ConsumeSMS
from telegram import ConsumeTelegram
from telegram_h1 import ConsumeHTlgrmOne
from telegram_h2 import ConsumeHTlgrmTwo


def Supervisor(thr_list):
    thr = []

    for thread_name in thr_list:
        thr.append(None)

    while True:
        i = 0
        for thread_name in thr_list:
            if not thr[i] or not thr[i].is_alive():
                thr[i] = Thread(target=thread_name)
                thr[i].daemon = True
                thr[i].start()
                syslog.syslog("Starting thread for: %s" % str(thread_name))
                print("Starting thread for: %s" % str(thread_name))
            thr[i].join(1)
            i = i + 1

        time.sleep(10)


if __name__ == "__main__":
    syslog.openlog('some_tag', syslog.LOG_PID, syslog.LOG_NOTICE)

    try:
        thr_list = [
            ConsumeOne().start_consume_one,
            ConsumeTwo().start_consume_two,
            ConsumeThree().start_consume_three,
            ConsumeMail().start_consume_mail,
            ConsumeSMS().start_consume_sms,
            ConsumeTelegram().start_consume_telegram,
            ConsumeHTlgrmOne().start_consume,
            ConsumeHTlgrmTwo().start_consume
        ]


        Supervisor(thr_list)


    except KeyboardInterrupt:

        print("EXIT")

        raise