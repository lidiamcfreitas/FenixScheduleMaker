import urllib.request
import string

# https://fenix.tecnico.ulisboa.pt/disciplinas/TCom511/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/IPM2011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/EO1011/2014-2015/2-semestre
# https://fenix.tecnico.ulisboa.pt/disciplinas/ASA764511/2014-2015/2-semestre

# https://fenix.tecnico.ulisboa.pt/disciplinas/PEst11645/2014-2015/2-semestre

def processTime(timeString):
    dayString = timeString[:3]
    timeString = timeString[timeString.find(":")-2:]
    beginString = timeString[:5]
    timeString = timeString[3:]
    endString = timeString[timeString.find(":")-2:]
    
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
            self.diyCourse += [[self.name+"T"+num, "    ", day+", "+begin+" something "+end+""]]

        
        def addProblemas(self,day,num, begin, end):
            self.diyCourse += [[self.name+"PB"+num, "    ", day+", "+begin+" something "+end+""]]  

        def actualize(self):
            self.input = self.diyCourse
            self.shifts = processCourse(self.name,self.diyCourse)            
        
        

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
c.actualize()
x.addCourse(c)



#x.insertUrl()
#x.insertUrl()
#x.insertUrl()    
#x.insertUrl()

#x.printObjects()
    