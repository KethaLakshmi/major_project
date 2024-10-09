class Student:
    def __init__(self, name, roll_number,classs,section):
        self.name = name
        self.roll_number = roll_number
        self.classs=classs
        self.section=section
        self.grades={}
    def add_grades(self,grade,subject):
        self.subject=subject
        self.grade=grade
        self.grades[subject]=grade 
        return self.grades
    def display_info(self):
        return {
            "name": self.name,
            "class":self.classs,
            "section":self.section,
            "roll_number": self.roll_number,
        }


class StudentTracker:
    def __init__(self):
        self.students = {}

    def add_student(self, name, roll_number,classs,section):
        if roll_number not in self.students:
            self.students[roll_number] = Student(name, roll_number,classs,section)
        else:
            raise ValueError("Student with this roll number already exists.")
    def add_grades(self,roll_number,subject,grade):
        if roll_number in self.students:
            return self.students[roll_number].add_grades(grade,subject)
    def view_student_details(self, roll_number):
        if roll_number in self.students:
            return self.students[roll_number].display_info()
        else:
            raise ValueError("Student not found.")
    def cal_average(self, roll_number):
        if roll_number in self.students:
            student = self.students[roll_number]
            if student.grades:  # Check if there are any grades
                average = sum(student.grades.values()) / len(student.grades)
                return average
            else:
                return 0  # No grades available    


