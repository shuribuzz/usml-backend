import syslog
import time
from threading import Thread
from handler import Handler


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

    thr_list = []
    list_queue = [
            "queue_one",
            "queue_two",
            "queue_three",
            "queue_mail",
            "queue_sms",
            "queue_tlgrm",
            "queue_Tgm_1"
            ]

    try:
        for n in list_queue:
            t = Handler(n)
            thr_list.append(t.start_consume)

        Supervisor(thr_list)

    except KeyboardInterrupt:
        print("EXIT")
        raise
