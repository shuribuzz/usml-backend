from queue import Queue
import threading
from time import sleep
from time import time
from damn_people import ret_people

list_people = ret_people()
#list_people = {'hum1': 'Pain', 'hum2': 'Deadline', 'hum3': 'Pain', 'hum4': 'Deadline'}
#list_people = {'hum1': 'Deadline', 'hum2': 'Pain', 'hum3': 'Thirst', 'hum4': 'Insomnia'}
q_pain = Queue()
q_thirst = Queue()
q_insomnia = Queue()
q_deadline = Queue()

def teambuild(list_people):
    for hum in list_people:
        if list_people.get(hum) == 'Pain':
            sleep(1)
            print(hum + ' is pain')
            q_pain.put('Pain')
        elif list_people.get(hum) == 'Thirst':
            sleep(1)
            print(hum + ' is thirst')
            q_thirst.put('Thirst')
        elif list_people.get(hum) == 'Insomnia':
            sleep(1)
            print(hum + ' is insomnia')
            q_insomnia.put('Insomnia')
        elif list_people.get(hum) == 'Deadline':
            sleep(1)
            print(hum + ' is deadline')
            q_deadline.put('Deadline')

def healer(q, n):
    while True:
        item = q.get()
        if item == 'Pain':
            sleep(5)
            print('relieved of pain! {}'.format(n))
        elif item == 'Thirst':
            sleep(5)
            print('relieved of thirst! {}'.format(n))
        elif item == 'Insomnia':
            sleep(5)
            print('relieved of insomnia! {}'.format(n))
        elif item == 'Deadline':
            sleep(5)
            print('relieved of deadline! {}'.format(n))

        if item is None:
            break

teambuild(list_people)
t1 = threading.Thread(target=healer, args=(q_pain, 1))
t2 = threading.Thread(target=healer, args=(q_thirst, 2))
t3 = threading.Thread(target=healer, args=(q_insomnia, 3))
t4 = threading.Thread(target=healer, args=(q_deadline, 4))

t1.start()
t2.start()
t3.start()
t4.start()

q_pain.put(None)
q_thirst.put(None)
q_insomnia.put(None)
q_deadline.put(None)

t1.join()
t2.join()
t3.join()
t4.join()
