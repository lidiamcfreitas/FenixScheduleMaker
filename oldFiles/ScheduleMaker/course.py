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
