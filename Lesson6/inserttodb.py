import sqlite3
from scrap import ret_courses
from time import time

t0 = time()
list = ret_courses()

#Создаем соединение с нашей базой данных
connect_db = sqlite3.connect('db.sqlite')

# Создаем курсор
cursor = connect_db.cursor()

# Делаем INSERT запрос к базе данных
for items in list:
    cursor.execute('INSERT INTO curses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )', items)

#Cохраняем транзакцию и закрываем соединение с ДБ
connect_db.commit()
print('База данных создана')
connect_db.close()

t1 = time()

print("Timer is %s seconds" % (t1-t0))
