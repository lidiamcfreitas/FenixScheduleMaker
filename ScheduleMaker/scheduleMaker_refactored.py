""" main module for the schedule maker"""

import urllib.request
from tkinter import *
import presentation
import sys
from schedule import *
from course import *

numSchedules = 0

def combineCourse2(course1, course2):
    """ TODO make docstring """
    #print(2*'\n\t',course1, course2)
    master = [course1, course2]
    # group = []

    n = len(master)
    # count = 0
    # defaultL = [("None", 0, 0)]
    # defaultP = [("Nune", 0, 0)]
    # defaultT = [("Nane", 0, 0)]

    if n <= 0:
        print("do a real course")

    else:
        tipoAula1 = master[0]
        for tipoAula2 in master:
            if tipoAula2 == master[0]:
                continue
            else:
                #print(len(tipoAula1))
                #print(len(tipoAula2))
                tipoAula1 = combine(tipoAula1, tipoAula2)

    return  tipoAula1


def combineCourse(course):
    """ TODO make docstring """

    defaultL = [("None", 0, 0)]
    defaultP = [("Nune", 0, 0)]
    # defaultT = [("Nane", 0, 0)]
    t = course.getTeoricas()
    pb = course.getProblemas()

    if len(pb) == 0:
        pb = [defaultP]

    l = course.getLabs()
    if len(l) == 0:
        l = [defaultL]

    master = [t, pb, l]
    #print(master)
    # group = []

    n = len(master)
    # count = 0

    if n <= 0:
        print("fuck off, do a real course")

    else:
        tipoAula1 = master[0]
        for tipoAula2 in master:
            if tipoAula2 == master[0]:
                continue
            else:
                #print(len(tipoAula1))
                #print(len(tipoAula2))
                tipoAula1 = combine(tipoAula1, tipoAula2)

    return tipoAula1

def combine(aula1, aula2):
    """ TODO make docstring """
    grupo = []

    for turma1 in aula1:
        for turma2 in aula2:
            #print(len(turma1), len(turma2), (turma1),(turma2))
            teste = combineTurmas(turma1, turma2)

            if teste == -1:
                continue
            else:
                grupo += [teste]

    return grupo

def combineTurmas(turma1, turma2):
    """ TODO make docstring """

    if len(turma1) == 0 or len(turma2) == 0:
        raise Exception("I know python!")

    for hora1 in turma1:
        for hora2 in turma2:
            if hora1[0] == hora2[0]: #mesmo dia
                if not possibleToCombine(hora1[1], hora1[2], hora2[1], hora2[2]):
                    return -1

    #print("\t", turma1, turma2)
    '''
    if len(turma1))==1 and len(turma2)==1:
        return [turma1[0], turma2[0]]
    elif len(turma1)==1:
        return turma1[0] + turma2
    elif len(turma2)==1:
        return turma1 + turma2[0]
    return '''
    return turma1 + turma2


def possibleToCombine(min1, max1, min2, max2):
    """ TODO make docstring """
    return max1 <= min2 or max2 <= min1

def printVect(vectToPrint):
    """ TODO make docstring """
    s = ""
    for arr in vectToPrint:
        if isinstance(arr, tuple):
            return "\t" + str(arr[0]) +" "+ str(arr[1]) +" "+ str(arr[2])
        else:
            s += printVect(arr)
        s += '\n'
    return  s+'\n'

def graph():
    global B
    master = Tk()
    time = 8
    days=["Seg","Ter","Qua","Qui","Sex","Sab","Dom"]
    dayCounter = 0

    w = Canvas(master, width=1200, height=620)
    w.pack()

    #w.create_line(0, 0, 200, 100)
    #w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    for i in range(7):
        w.create_line(i*200, 0, i*200, 600)
        w.create_text(i*200+300, 12, text=days[dayCounter])
        dayCounter += 1

    for i in range(25):
        w.create_line(0, i*25, 1200, i*25)
        w.create_text(100, 12+(i+1)*25, text=str(time))
        time += 0.5

    # text entry : E1 = Entry(width=100).pack(side=LEFT)



    B1 = Button(text="Next", command=lambda: graphSchedule(w)).pack(side=RIGHT)
    B2 = Button(text="Exit", command=lambda: sys.exit(0)).pack(side=RIGHT)
    B3 = Button(text="Previous", command=lambda: previousSchedule(w)).pack(side=RIGHT)
    B4 = Button(text="Save", command=lambda: save(w)).pack(side=RIGHT)

    mainloop()

def save(w):
    w.update()
    w.postscript(file = "save.ps")

def deleteCanvas(w):
    """ TODO make docstring """
    w.delete("d")

def previousSchedule(w):
    """ TODO make docstring """
    global numSchedules
    deleteCanvas(w)

    if numSchedules != 0:
        numSchedules -= 2
        graphSchedule(w)
    else:
        return


def graphSchedule(w):
    """ TODO make docstring """
    global numSchedules
    deleteCanvas(w)
    shifthours = -7

    case = array[numSchedules]

    if numSchedules != len(array)-1:
        numSchedules += 1
    else:
        return
    #print(numSchedules, case)


    height = 1200
    for aula in case:
        if aula[0] == "Seg":
            w.create_rectangle(200, (aula[1]+shifthours)/24*height, 400, (aula[2]+shifthours)/24*height, fill="grey", tags="d")
            #print(aula)
            w.create_text(300, (aula[1]+aula[2]+shifthours*2)/48*height, text=aula[3]+ aula[4], tags="d")

        if aula[0] == "Ter":
            w.create_rectangle(400, (aula[1]+shifthours)/24*height, 600, (aula[2]+shifthours)/24*height, fill="grey", tags="d")
            w.create_text(500, (aula[1]+aula[2]+shifthours*2)/48*height, text=aula[3]+ aula[4], tags="d")
            #print(aula)

        if aula[0] == "Qua":
            w.create_rectangle(600, (aula[1]+shifthours)/24*height, 800, (aula[2]+shifthours)/24*height, fill="grey", tags="d")
            w.create_text(700, (aula[1]+aula[2]+shifthours*2)/48*height, text=aula[3]+ aula[4], tags="d")
            #print(aula)

        if aula[0] == "Qui":
            w.create_rectangle(800, (aula[1]+shifthours)/24*height, 1000, (aula[2]+shifthours)/24*height, fill="grey", tags="d")
            w.create_text(900, (aula[1]+aula[2]+shifthours*2)/48*height, text=aula[3]+ aula[4], tags="d")
            #print(aula)

        if aula[0] == "Sex":
            w.create_rectangle(1000, (aula[1]+shifthours)/24*height, 1200, (aula[2]+shifthours)/24*height, fill="grey", tags="d")
            w.create_text(1100, (aula[1]+aula[2]+shifthours*2)/48*height, text=aula[3]+ aula[4], tags="d")
            #print(aula)

'''
Example of doing it by hand
c = Course("PE1234",[])
c.addTeorica("Seg","01","17:30","19:00")
c.addTeorica("Ter","01","17:30","19:00")
c.addTeorica("Seg","02","16:00","17:30")
c.addTeorica("Ter","02","16:00","17:30")

c.addProblemas("Qui","03","14:30","16:00")
c.addProblemas("Sex","04","14:30","16:00")
c.addProblemas("Seg","05","14:30","16:00")
c.addProblemas("Qua","06","17:30","19:00")
c.addProblemas("Sex","07","13:00","14:30")'''

"""
c = Course("PE1234",[])
c.addTeorica("Seg","01","17:30","19:00")
c.addTeorica("Ter","01","17:30","19:00")

c.addProblemas("Qui","03","14:30","16:00")
c.addProblemas("Sex","04","14:30","16:00")
c.addProblemas("Seg","05", "18:00", "19:00")


#c.addLabs("Qua","06","20:30","22:00")
c.addLabs("Sab","07","05:00","06:30")
c.addLabs("Sex","08","15:00","16:00")


c.actualize()
x.addCourse(c)
"""

x = Schedule()

present = presentation.Presentation()
for url in present.log.getCoursesUrls()[0]:
    x.insertUrl(url)

array = []
def makeArray():
    """ TODO make docstring """
    global array
    array = combineCourse2(combineCourse(x.objects[0]), combineCourse(x.objects[1]))
    for i in range(2, len(x.objects)):
        array = combineCourse2(array, combineCourse(x.objects[i]))

#x.printObjects()

def sortSmallestIntervall():
    """ TODO make docstring """
    global array
    sortedDays = ['Dom', 'Qua', 'Qui', 'Sab', 'Seg', 'Sex', 'Ter']
    intervalArray = [0]*7

    for i in range(len(array)):

        array[i] = sorted(array[i], key=lambda classSche: classSche[0])
        array[i][:] = [x for x in array[i] if x != ('Nune', 0, 0) and x!= ('None', 0, 0)]
        numDay = 0
        intervalArray = [0]*7

        for classNum in range(len(array[i])):
            while numDay != 7:
                if array[i][classNum][0] != sortedDays[numDay]:
                    # if the day is different from the one in the array, continue
                    numDay += 1
                else:
                    if intervalArray[numDay] == 0:
                        intervalArray[numDay] = (array[i][classNum][1], array[i][classNum][2])
                        break
                    else:
                        if intervalArray[numDay][0] > array[i][classNum][1]: #first to start
                            first = array[i][classNum][1]
                        else:
                            first = intervalArray[numDay][0]
                        if intervalArray[numDay][1] > array[i][classNum][2]: #first to finish
                            last = intervalArray[numDay][1]
                        else:
                            last = array[i][classNum][2]
                        intervalArray[numDay] = (first, last)
                        break
        timeSum = 0
        iniTime = 0 #time when classes start
        for elem in intervalArray:
            if elem!=0:
                timeSum += (elem[1]-elem[0])
                iniTime += elem[0]
        array[i] = [timeSum, iniTime]+array[i]


    array = sorted(array, key=lambda classSche: (classSche[0], classSche[1]))
    # sort first by sum of time and then by initials

    for i in range(len(array)):
        array[i] = array[i][2:]

def menuChooseClass():
    """ TODO make docstring """
    x.printCoursesNames()
    courseOption = input('Escolhe o numero da cadeira: ')
    print(x.objects[int(courseOption)].shifts)
    printShifts(x.objects[int(courseOption)].shifts)
    print(0, "Teorica")
    print(1, "Pratica")
    print(2, "Lab")
    typeOption = input('Escolhe o numero do tipo de aula: ')
    print(x.objects[int(courseOption)].shifts[int(typeOption)])
    classOption = input('Escolhe o turno, por exemplo L01: ')
    print(x.objects[int(courseOption)].shifts[int(typeOption)][classOption])
    newDic = {}
    newDic[classOption] = x.objects[int(courseOption)].shifts[int(typeOption)][classOption]
    x.objects[int(courseOption)].shifts[int(typeOption)] = newDic

    makeArray()
    sortSmallestIntervall()
    return
makeArray()
sortSmallestIntervall()
graph()
