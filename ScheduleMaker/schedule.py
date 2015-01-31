import urllib.request
import string

# https://fenix.tecnico.ulisboa.pt/disciplinas/TCom511/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/IPM2011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/EO1011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/ASA764511/2014-2015/2-semestre

# https://fenix.tecnico.ulisboa.pt/disciplinas/PEst11645/2014-2015/2-semestre

def processTime(timeString):
    dayString = timeString[:3] # gets day from timeString
    timeString = timeString[timeString.find(":")-2:]
    beginString = timeString[:5] #gets begining of class
    timeString = timeString[3:]  
    endString = timeString[timeString.find(":")-2:] # gets end of class
    
    begin = int(beginString[:2]) + int(beginString[-2:])/60
    end = int(endString[:2]) + int(endString[-2:])/60
    return tuple((dayString,begin,end))


def processCourse(courseName,course = []):
    classTypes = [{},{},{}]
    for courseClass in course:
        shift = courseClass[0][len(courseName):]
        time = processTime(courseClass[2])
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
                
                
    
def combineCourse(course):
    t = course.getTeoricas()
    pb = course.getProblemas()
    l = course.getLabs()
    possibles = []
    possible = []
    group = []
    count = 0

    for teorica in t:
        #print("cenas 1.1")
        for problemas in pb:
            #print("cenas 1.2")
            for labs in l:
                #print("cenas 1.3")
                test = combine(teorica, problemas, labs)
                if test == -1:
                    break;

                count +=1
                print(count, test)
                group += test
                
    
    return group

def combine(teorica, problemas, labs):
    combos = []
    
    for t_aula in teorica:
        #print(t_aula[0])
        for pb_aula in problemas:
            #print(pb_aula[0])
            if t_aula[0] == pb_aula[0]:  # mesmo dia T e PB
                if not possibleToCombine(t_aula[1], t_aula[2], pb_aula[1], pb_aula[2]):
                    return -1
                for l_aula in labs:
                    #print("cenas 3")
                    if t_aula[0] == l_aula[0]: # mesmo dia T e L
                        if possibleToCombine(t_aula[1], t_aula[2], l_aula[1], l_aula[2]) and possibleToCombine(pb_aula[1], pb_aula[2], l_aula[1], l_aula[2]):
                            combos += [(teorica, problemas, labs)] #adiciona
                        else:
                            return -1
                    else:
                        if not possibleToCombine(pb_aula[1], pb_aula[2], t_aula[1], t_aula[2]):
                            return -1
                        else:
                            combos += [(teorica, problemas, labs)] #adiciona                          
            else: # diferente dia T e PB
                for l_aula in labs:
                    #print("cenas 3")
                    if pb_aula[0] == l_aula[0]: # mesmo dia PB e L
                        if not possibleToCombine(pb_aula[1], pb_aula[2], l_aula[1], l_aula[2]):
                            return -1
                        else:
                            combos += [(teorica, problemas, labs)] # adiciona
                    else: # diferente dia PB e L
                        if l_aula[0] == t_aula[0]:
                            if not possibleToCombine(l_aula[1], l_aula[2], t_aula[1], t_aula[2]):
                                return -1
                            else:
                                combos += [(teorica, problemas, labs)] #adiciona                            
                
                
    return [(teorica, problemas, labs)]


def possibleToCombine(min1, max1, min2, max2):
    
    return (max1 < min2 or max2 < min1)

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

c = Course("PE1234",[])
c.addTeorica("Seg","01","17:30","19:00")
c.addTeorica("Ter","01","17:30","19:00")
c.addTeorica("Seg","02","16:00","17:30")
c.addTeorica("Ter","02","16:00","17:30")

c.addProblemas("Qui","03","14:30","16:00")
c.addProblemas("Sex","04","14:30","16:00")
c.addProblemas("Seg","05","14:30","16:00")
c.addProblemas("Qua","06","17:30","19:00")
c.addProblemas("Sex","07","13:00","14:30")

c.addLabs("Qua","06","20:30","22:00")
c.addLabs("Sex","07","05:00","06:30")


c.actualize() 
x.addCourse(c)


#x.insertUrl()
#x.insertUrl()
#x.insertUrl()    
#x.insertUrl()

x.printObjects()



# combineCourse(x.objects[0])