import random

d ={}
hum_list = []
hum_curse_list = []
curse = ['Pain', 'Thirst', 'Insomnia', 'Deadline']


for n in range(1,31):
    hum_list.append('hum' + str(n))

for hum in hum_list:
    k = str(hum)
    d[k] = 'good'

def ret_people():
    count = 0
    for hum in hum_list:
        while count < 10:
            k = random.choice(list(d.keys()))
            if d[k] == 'good':
                d[k] = random.choice(curse)
            else:
                continue
            count += 1

    return d
