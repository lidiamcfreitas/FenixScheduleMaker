""" this is the module for the schedule implementation """

import urllib.request
import logging
from course import Course
logger = logging.getLogger()

def printShifts(shift=None):
    """ print shifts """
    counter = 0
    if shift is None:
        return
    for classtype in shift:
        for key in classtype.keys():
            print(counter, key)
            counter += 1
            for time in classtype[key]:
                print("\t", time[0:])


def findCourseNameInUrl(filename):
    """retorna o indicativo da cadeira"""
    start = filename.find("disciplinas/")
    end = filename[start+len("disciplinas/"):].find("/")

    return filename[start + len("disciplinas/"):start + len("disciplinas/")+ end]

def codeFromUrl(filename):
    """cleans the given url and gets the code"""
    deleteAfter = filename.find("semestre")
    filename = filename[:deleteAfter + len("semestre")]+ "/turnos"

    response = urllib.request.urlopen(filename)
    return (findCourseNameInUrl(filename), response.read().decode('utf-8'))


class Schedule:
    """ This class represents a schedule which has courses"""

    objects = []

    def __init__(self):
        print("Empty schedule created.")


    def insertUrl(self, filename=None):
        """insert course with url"""
        if filename is None:
            filename = input('Enter an url: ')

        string = codeFromUrl(filename)[1]
        courseName = codeFromUrl(filename)[0]


        code = 1
        counter = 0
        course = []

        while code != -1:
            newSchedule = []
            for counter in range(5):
                code = string.find("<td>")
                end = string[code:].find("</td>")
                if counter < 3:
                    newSchedule += [string[code+ len("<td>"):code+end]]
                    #print(string[code+ len("<td>"):code+end])
                string = string[code+1:]
                code = string.find("<td>")
                counter += 1
            course += [newSchedule]

        self.objects.append(Course(courseName, course))


    def printObjects(self):
        """print object shifts"""
        for obj in self.objects:
            print(30*"_ " + obj.name + 30*" _")
            print()
            printShifts(obj.shifts)

    def printCoursesNames(self):
        """print courses names"""
        for i_obj in range(len(self.objects)):
            print(i_obj, self.objects[i_obj].name)

    def addCourse(self, course):
        """ add course """
        self.objects += [course]

    # def combineSchedules(self):
    #     """ combines schedules"""
    #     return
