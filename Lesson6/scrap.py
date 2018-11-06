import json
import urllib
import re
from urllib.request import *

categories_list = []
disciplines_list = []
curse_list = []
test_list = [3039, 4006]
courses = []
courses_clean = []

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def ret_courses():
    for n in range(28):
        try:
            responce = urlopen('https://stepik.org:443/api/course-lists/' + str(n)).read()
            responceJson = json.loads(responce)
            #categories_list.append(responceJson.get('course-lists')[0].get('title'))
            disciplines_list.append(responceJson.get('course-lists')[0].get('courses'))


        except urllib.error.HTTPError as error:
            if error.code == 404:
                None
            else:
                raise

    for disciplines in disciplines_list:
        for curse_id in disciplines:
            courses_item = []
            resp_cat = urlopen('https://stepik.org:443/api/courses/' + str(curse_id)).read()
            resp_catJson = json.loads(resp_cat)
            '''
            print('Название курса: {}'.format(resp_catJson.get('courses')[0].get('title')))
            print('Цель курса: {}'.format(resp_catJson.get('courses')[0].get('summary')))
            print('Описание курса: {}'.format(resp_catJson.get('courses')[0].get('description')))
            print('Требования: {}'.format(resp_catJson.get('courses')[0].get('requirements')))
            print('Целевая аудитория: {}'.format(resp_catJson.get('courses')[0].get('target_audience')))
            print('Нагрузка: {}'.format(resp_catJson.get('courses')[0].get('workload')))
            print('Дата начала: {}'.format(resp_catJson.get('courses')[0].get('begin_date')))
            print('Сертификат: {}'.format(resp_catJson.get('courses')[0].get('certificate')))
            '''
            courses_item.append(resp_catJson.get('courses')[0].get('id'))
            courses_item.append(resp_catJson.get('courses')[0].get('title'))
            courses_item.append(resp_catJson.get('courses')[0].get('summary'))
            courses_item.append(cleanhtml(resp_catJson.get('courses')[0].get('description')))
            courses_item.append(cleanhtml(resp_catJson.get('courses')[0].get('requirements')))
            courses_item.append(resp_catJson.get('courses')[0].get('target_audience'))
            courses_item.append(resp_catJson.get('courses')[0].get('workload'))
            courses_item.append(resp_catJson.get('courses')[0].get('begin_date'))
            courses_item.append(resp_catJson.get('courses')[0].get('certificate'))
            instructors_list = resp_catJson.get('courses')[0].get('instructors')
            instructors = []
            for instructor in instructors_list:
                resp_instr = urlopen('https://stepik.org:443/api/users/' + str(instructor)).read()
                resp_instrJson = json.loads(resp_instr)
                instructors.append(resp_instrJson.get('users')[0].get('full_name'))
            courses_item.append(str(instructors))
            courses.append(courses_item)

    for i in courses:
        if i not in courses_clean:
            courses_clean.append(i)


    return courses_clean
