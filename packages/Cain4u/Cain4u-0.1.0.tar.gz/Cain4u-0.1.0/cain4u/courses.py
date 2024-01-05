class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self): # def __str(self): 
        return f"{self.name} [{self.duration}] horas {self.link} "
courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-linux"),
    Course("Personalizacion de Linux", 3,"https://hack4u.io/cursos/personalizacion-linux" ),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/Introduccion-Hacking")
]

#for course in courses:
#    print(course)
def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course
    return None


