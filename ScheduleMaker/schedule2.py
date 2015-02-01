import urllib.request
import string
from tkinter import *

# https://fenix.tecnico.ulisboa.pt/disciplinas/TCom511/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/IPM2011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/EO1011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/ASA764511/2014-2015/2-semestre

# https://fenix.tecnico.ulisboa.pt/disciplinas/PEst11645/2014-2015/2-semestre


def processTime(courseClass, courseName):
    timeString = courseClass[2]
    dayString = timeString[:3] # gets day from timeString
    timeString = timeString[timeString.find(":")-2:]
    beginString = timeString[:5] #gets begining of class
    timeString = timeString[3:]  
    endString = timeString[timeString.find(":")-2:] # gets end of class
    
    begin = int(beginString[:2]) + int(beginString[-2:])/60
    end = int(endString[:2]) + int(endString[-2:])/60
    
    return tuple((dayString,begin,end, courseName))


def processCourse(courseName,course = []):
    classTypes = [{},{},{}]
    for courseClass in course:
        shift = courseClass[0][len(courseName):]
        time = processTime(courseClass, courseName)
        print(time)
        if shift.find("T") == 0:
            
            if shift in classTypes[0].keys():
                classTypes[0][shift] += [time]
            else:
                classTypes[0][shift] = [time]
        if shift.find("PB") == 0:
            
            if shift in classTypes[1].keys():
                classTypes[1][shift] += [time]
            else:
                classTypes[1][shift] = [time]        
        if shift.find("L") == 0:
            
            if shift in classTypes[1].keys():
                classTypes[2][shift] += [time]
            else:
                classTypes[2][shift] = [time]
    
    return classTypes
    
    
def codeFromUrl(filename):
    deleteAfter = filename.find("semestre")
    filename = filename[:deleteAfter + len("semestre")]+ "/turnos"
    
    response = urllib.request.urlopen(filename)
    return response.read().decode('utf-8')  


def findCourseNameInUrl(filename):
        
        start = filename.find("disciplinas/")
        end = filename[start+len("disciplinas/"):].find("/")

        return filename[start + len("disciplinas/"):start + len("disciplinas/")+ end]
    
def printShifts(shift = []):
    for classtype in shift:
        for key in classtype.keys():
            print(key)
            for time in classtype[key]:
                print("\t",time[0:])
                
                
    
def combineCourse2(course1, course2):
    print(2*'\n\t',course1, course2)
    master = [course1,course2]
    group = []
    
    n = len(master)
    count=0
    defaultL = [("None", 0,0)]
    defaultP = [("Nune",0,0)]
    defaultT = [("Nane",0,0)]

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
                tipoAula1 = combine(tipoAula1,tipoAula2)
                

    return  tipoAula1
    
    
def combineCourse(course):
    defaultL = [("None", 0,0)]
    defaultP = [("Nune",0,0)]
    defaultT = [("Nane",0,0)]
    t = course.getTeoricas()
    pb = course.getProblemas()
    if len(pb)==0:
        pb=[defaultP]
    
    l = course.getLabs()
    if len(l)==0:
        l=[defaultL]
    
    master = [t,pb,l]
    print(master)
    group = []
    
    n = len(master)
    count=0

    if n <= 0:
        print("fuck off, do a real course")
        
    else:
        tipoAula1 = master[0]
        for tipoAula2 in master:
            if tipoAula2 == master[0]:
                continue
            else:
                print(len(tipoAula1))
                print(len(tipoAula2))
                tipoAula1 = combine(tipoAula1,tipoAula2)
                

    return tipoAula1

def combine(aula1, aula2):
    grupo = []
    teste = []
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
    
    if len(turma1)==0 or len(turma2)==0:
        raise Exception("I know python!")
    
    for hora1 in turma1:
        for hora2 in turma2:
            if hora1[0] == hora2[0]: #mesmo dia
                if not possibleToCombine(hora1[1],hora1[2],hora2[1],hora2[2]):
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
    
    return (max1 <= min2 or max2 <= min1)

def printVect(vectToPrint):
    
    s = ""
    for array in vectToPrint:
        if isinstance(array, tuple):
            return "\t" + str(array[0]) +" "+ str(array[1]) +" "+ str(array[2])
        else:
            s += printVect(array)
        s += '\n'
    return  s+'\n'
    


class Course:
    
        name = ""
        input = []
        shifts = {}
        
        diyCourse = []
        
        def __init__(self, name, course = []):
            print("new course created!")
            self.name = name
            self.input = course
            self.shifts = processCourse(self.name,course)
        
        def addTeorica(self,day,num, begin, end):
            self.diyCourse += [[self.name+"T"+num," ",day+", "+begin+end]]
            self.actualize() 

        
        def addProblemas(self,day,num, begin, end):
            self.diyCourse += [[self.name+"PB"+num," ",day+", "+begin+end]] 
            self.actualize()

        def addLabs(self,day,num, begin, end):
            self.diyCourse += [[self.name+"L"+num," ",day+", "+begin+end]] 
            self.actualize()


        def actualize(self):
            self.input = self.diyCourse
            self.shifts = processCourse(self.name,self.diyCourse)
        
        def getTeoricas(self):
            res = []
            for key in self.shifts[0]:
                res += [self.shifts[0][key]]
                        
            return res
        
        def getProblemas(self):
            res = []
            for key in self.shifts[1]:
                res += [self.shifts[1][key]]            
            return res
        
        def getLabs(self):
            res = []
            for key in self.shifts[2]:
                res += [self.shifts[2][key]]
            return res
        

class Schedule:
    
    objects = []
    
    def __init__(self):
        print("Hello there champ!")
        
    
    def insertUrl(self):
        filename = input('Enter an url: ')
        #filename = "https://fenix.tecnico.ulisboa.pt/disciplinas/ACED58511/2014-2015/2-semestre/turnos"
        
        print("")
        
        string = codeFromUrl(filename)
        courseName = findCourseNameInUrl(filename)
        
        
        code = 1
        counter = 0
        course = []
        
        while ( code != -1):
            newSchedule = []
            #print()
            for counter in range(5):
                code = string.find("<td>")
                end = string[code:].find("</td>")
                if counter < 3:
                    newSchedule += [string[code+ len("<td>"):code+end]]
                    #print(string[code+ len("<td>"):code+end])
                string = string[code+1:]
                code = string.find("<td>")
                counter +=1
            course += [newSchedule]
    
        self.objects.append(Course(courseName, course))
        
    def printObjects(self):
        for obj in self.objects:
            print(30*"_ " + obj.name + 30*" _")
            print()
            printShifts(obj.shifts)
            
    def addCourse(self, course):
        self.objects += [course]
        
    def combineSchedules(self):
        
        return 

x = Schedule()
'''
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

array = combineCourse(x.objects[0])[0]
print(array)


#x.insertUrl()
#x.insertUrl()
#x.insertUrl()    
#x.insertUrl()

#x.printObjects()



# combineCourse(x.objects[0])

def graph():
    master = Tk()
    
    w = Canvas(master, width=1000, height=600)
    w.pack()
    
    #w.create_line(0, 0, 200, 100)
    #w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    
    for i in range(6):
        w.create_line(i*200,0,i*200,600)
        
    for i in range(24):
        w.create_line(0,i*25,1000,i*25)
          
    
    for aula in array:
        if aula[0] == "Seg":
            w.create_rectangle(0,aula[1]/24*600, 200, aula[2]/24*600, fill="red")
        if aula[0] == "Ter":
            w.create_rectangle(200,aula[1]/24*600, 400, aula[2]/24*600, fill="red")
        if aula[0] == "Qua":
            w.create_rectangle(400,aula[1]/24*600, 600, aula[2]/24*600, fill="red")
        if aula[0] == "Qui":
            w.create_rectangle(600,aula[1]/24*600, 800, aula[2]/24*600, fill="red")
        if aula[0] == "Sex":
            w.create_rectangle(800,aula[1]/24*600, 1000, aula[2]/24*600, fill="red") 
            
    t = Label(w, text="Hello John, Michael, Eric, ...", anchor='w')
    
    mainloop() 


#w.create_line(0, 0, 100, 100, fill="blue")
#w.create_line(0,100, 200, 100, fill="red")


