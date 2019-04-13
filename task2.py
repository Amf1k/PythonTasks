import json
import collections
from operator import itemgetter
from threading import Thread
import multiprocessing.dummy as multiprocessing


def top10most_difficult():
    peoplesArray = loadJson()
    dictSubjectAndCount = collections.Counter()  # предмет и кол-во оценок по нему
    dictSubjectAndMark = collections.Counter()  # предмет и сумма оценок по нему
    dictSubjectAndAverage = {}  # предмет и средняя оценка по нему
    for d in peoplesArray:
        dictSubjectAndCount[d['subject']] += 1
        dictSubjectAndMark[d['subject']] += (d['mark'])
    for names in list(dictSubjectAndCount.keys()):
        dictSubjectAndAverage[names] = dictSubjectAndMark[names] / dictSubjectAndCount[names]

    #     отсортировать словарь по значению и выбрать первые 10:
    c = collections.Counter(dictSubjectAndAverage).most_common()  # возвращает список с tuple ('предмет', ср.балл)
    c.reverse()
    print('\n10 самых трудных предметов:')
    for elem in c[:10]:
        print(elem[0])


# находим средний балл для студента


def top10performance():
    peoplesArray = loadJson()
    # сумма баллов по предметам
    marks = collections.Counter()
    # кол-во предметов
    counts = collections.Counter()
    performance = {}
    for people in peoplesArray:
        marks[people['name']] += people['mark']
        counts[people['name']] += 1
    for names in list(marks.keys()):
        performance[names] = marks[names] / counts[names]
    print("\nТоп 10 студентов по успеваемости:")
    for student in sorted(performance.items(), key=itemgetter(1), reverse=True)[:10]:
        print(student)


def top10_leave():
    peoplesArray = loadJson()
    # кол-во прогулов
    counts = collections.Counter()
    for people in peoplesArray:
        counts[people['name']] += people['leave']
    print("\nТоп 10 студентов по прогулам:")
    for student in counts.most_common()[:10]:
        print(student)


def linearSolution():
    top10most_difficult()
    top10performance()
    top10_leave()


def threadingSolution():
    thread1 = Thread(target=top10most_difficult())
    thread2 = Thread(target=top10performance())
    thread3 = Thread(target=top10_leave())
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


def processSolution():
    pool = multiprocessing.Pool()
    pool.map(lambda f: f(), [top10most_difficult])
    pool.map(lambda f: f(), [top10performance])
    pool.map(lambda f: f(), [top10_leave])
    pool.close()
    pool.join()


def addRecord():
    peoplesArray = loadJson()
    name = input('Введите ФИО\n')
    subject = input('Введите предмет\n')
    mark = int(input('Введите средний балл по предмету\n'))
    leave = int(input('Введите кол-во прогулов по предмету\n'))

    new_student = {'name': name, 'subject': subject, 'mark': mark, 'leave': leave}

    peoplesArray.append(new_student)

    new_json = {"peoples": peoplesArray}

    with open("json.json", "w") as write_file:
        json.dump(new_json, write_file)


def loadJson():
    jDict = json.load(open('json.json', 'r'))
    return jDict.get('peoples')  # возвращает список со словарями


n = input('\n1-линейное решение\n2-решение с потоками\n3-решение с процессами\n4-добавить запись в '
          'json\nexit-выход\nВвод ')

while n != 'exit':
    if n == '1':
        linearSolution()
    if n == '2':
        threadingSolution()
    if n == '3':
        processSolution()
    if n == '4':
        addRecord()
    if n == 'exit':
        break
    n = input('\n1-линейное решение\n2-решение с потоками\n3-решение с процессами\n4-добавить запись в'
              'json\nexit-выход\nВвод: ')
