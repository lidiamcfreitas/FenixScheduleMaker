""" module for the course implementation """

def processTime(courseClass, courseName):
    """ processes html time """
    timeString = courseClass[2]
    dayString = timeString[:3] # gets day from timeString
    timeString = timeString[timeString.find(":")-2:]
    beginString = timeString[:5] #gets begining of class
    timeString = timeString[3:]
    endString = timeString[timeString.find(":")-2:] # gets end of class

    begin = int(beginString[:2]) + int(beginString[-2:])/60
    end = int(endString[:2]) + int(endString[-2:])/60

    return tuple((dayString, begin, end, courseName))


def processCourse(courseName, course=None):
    """returns the classtypes, first 'teoricas', second 'problemas' and then 'labs'
    example: 'T01': [('Qui', 13.0, 14.5, 'ASA764511', 'T01'), ('Qui', 13.0, 14.5,
                  'ASA764511', 'T01'), ('Ter', 13.0, 14.5, 'ASA764511', 'T01')]"""
    if course is None:
        course = []

    classTypes = [{}, {}, {}]
    for courseClass in course:
        shift = courseClass[0][len(courseName):]
        time = processTime(courseClass, courseName)
        #print(time)
        if shift.find("T") == 0:
            if shift in classTypes[0].keys():
                classTypes[0][shift] += [time + (shift[:3],)]
            else:
                classTypes[0][shift] = [time+ (shift[:3],)]
        if shift.find("PB") == 0:

            if shift in classTypes[1].keys():
                classTypes[1][shift] += [time+ (shift[:4],)]
            else:
                classTypes[1][shift] = [time+ (shift[:4],)]
        if shift.find("L") == 0:

            if shift in classTypes[1].keys():
                classTypes[2][shift] += [time+ (shift[:3],)]
            else:
                classTypes[2][shift] = [time+ (shift[:3],)]


    return classTypes

class Course:
    """ class represents a course"""

    name = ""
    input = []
    shifts = {}

    diyCourse = []

    def __init__(self, name, course=None):
        if course is not None:
            print("new course created!")
            self.name = name
            self.input = course
            self.shifts = processCourse(self.name, course)

    def addTeorica(self, day, num, begin, end):
        """ adiciona teorica"""
        self.diyCourse += [[self.name+"T"+num, " ", day+", "+begin+end]]
        self.actualize()


    def addProblemas(self, day, num, begin, end):
        """ adiciona problemas """
        self.diyCourse += [[self.name+"PB"+num, " ", day+", "+begin+end]]
        self.actualize()

    def addLabs(self, day, num, begin, end):
        """ adiciona labs """
        self.diyCourse += [[self.name+"L"+num, " ", day+", "+begin+end]]
        self.actualize()


    def actualize(self):
        """ TODO cant remember """
        self.input = self.diyCourse
        self.shifts = processCourse(self.name, self.diyCourse)

    def getTeoricas(self):
        """retorna as teoricas"""
        res = []
        for key in self.shifts[0]:
            res += [self.shifts[0][key]]

        return res

    def getProblemas(self):
        """retorna as aulas de problemas"""
        res = []
        for key in self.shifts[1]:
            res += [self.shifts[1][key]]
        return res

    def getLabs(self):
        """retorna os laboratorios"""
        res = []
        for key in self.shifts[2]:
            res += [self.shifts[2][key]]
        return res
