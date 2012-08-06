class Student:
    def __init__(self, name="John Doe", age=18, year="Freshman", gpa=0.0):
        self.name = name
        self.age = age
        self.year = year
        self.gpa = gpa

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age

    def setYear(self, year):
        self.year = year

    def setGpa(self, gpa):
        self.gpa = gpa

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getYear(self):
        return self.year

    def getGpa(self):
        return self.gpa

class MaleStudent(Student):
    GENDER = "MALE"

    def getGender(self):
        return self.GENDER

class FemaleStudent(Student):
    GENDER = "FEMALE"

    def getGender(self):
        return self.GENDER

if __name__=="__main__":
    A = MaleStudent()
    B = FemaleStudent()
    print A.getGender()
    print B.getGender()


