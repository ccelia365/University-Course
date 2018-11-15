from collections import defaultdict
from prettytable import PrettyTable
import os
import sqlite3


class Student:
    """The Student Class holds all the details of a student, including cwid, name, major, course and grade"""

    stu_pt_header = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"]

    def __init__(self, cwid, name, major):
        """This method initializes a Student"""

        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grade = dict()

    def add_grade(self, course, grade):
        """This method adds a grade based on the course taken by the student in a dictionary"""

        self.course_grade[course] = grade

    def one_student(self, my_major):
        """This method creates a list for one row for the summary of one student"""
        # "CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"

        completed_courses, remaining_required, remaining_electives = my_major.completed_courses(self.course_grade)
        return [self.cwid, self.name, self.major, completed_courses, remaining_required, remaining_electives]

class Instructor:
    """The Instructor Class holds all details of an instructor, including the cwid, name, department, the course
    taught and the number of students in that particular course"""

    inst_pt_header = ["CWID", "Name", "Department", "Course", "Students"]

    def __init__(self, cwid, name, department):
        """This method initializes an Instructor"""

        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_student = defaultdict(int)  # dd[course] = number of students

    def add_course(self, course):
        """This method adds the students to the course taught in a dictionary"""

        self.course_student[course] += 1

    def one_instructor(self):
        """This method creates a list for one row for the summary of one instructor"""

        for course, student_num in self.course_student.items():
            yield [self.cwid, self.name, self.department, course, student_num]

def file_reader(path, num_of_field, sep='\t', header=False):
    """This method uses a generator and reads a text file separated by a pre-defined character"""

    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        print("Can't open", path)
    else:
        with fp:
            line_num = 1
            for line in fp:
                line = line.rstrip()
                if header == True and line_num == 1:
                    line_num += 1
                    continue
                else:
                    line_num += 1
                    my_line = line.split(sep)
                    my_count = len(my_line)
                    if my_count != num_of_field:
                        raise ValueError(path, "has", my_count, "fields on line", line, "but expected", num_of_field)
                    else:
                        my_line = tuple(my_line)
                        yield my_line

class Major:
    maj_pt_header = ["Dept", "Required", "Electives"]

    def __init__(self, major):
        """This method initializes a Major"""

        self.major = major
        self.course_req = set()
        self.course_elec = set()

    def add_course(self, flag, course):
        """ This method add a course depending on whether it is a required course or an elective """
        if flag == 'R':
            self.course_req.add(course)
        elif flag == 'E':
            self.course_elec.add(course)

    def completed_courses(self, courses):
        """This method calculates and returns completed_courses, remaining_required, remaining_electives given
        a dictionary with course and grades """

        completed_courses = {course for course, grade in courses.items() if
                             grade in ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')}
        remaining_required = self.course_req - completed_courses
        if self.course_elec.intersection(completed_courses):
            remaining_electives = None
        else:
            remaining_electives = self.course_elec

        return sorted(completed_courses), remaining_required, remaining_electives

    def one_major(self):
        """This method creates a list for one row for the summary of one major"""
        return [self.major, sorted(self.course_req), sorted(self.course_elec)]

class Repository:
    """This Repository Class holds students, instructors and grades"""

    def __init__(self, dir):
        """This method initializes a Repository"""

        self.cwid_student = dict()  # cwid_student [cwid] = Student ()
        self.cwid_instructor = dict()  # cwid_instructor [cwid] = Instructor ()
        self.major_course = dict()
        self.student_file(os.path.join(dir, "students.txt"))
        self.instructor_file(os.path.join(dir, "instructors.txt"))
        self.grade_file(os.path.join(dir, "grades.txt"))
        self.majors_file(os.path.join(dir, "majors.txt"))
        self.stu_pretty_table()
        self.inst_pretty_table()
        self.maj_pretty_table()

    def student_file(self, path):
        """This method reads the student text file and records the information in a dictonary"""

        for cwid, name, major in file_reader(path, num_of_field=3, sep='\t', header=False):
            self.cwid_student[cwid] = Student(cwid, name, major)

    def instructor_file(self, path):
        """This method reads the instructor text file and records the information in a dictonary"""

        for cwid, name, department in file_reader(path, num_of_field=3, sep='\t', header=False):
            self.cwid_instructor[cwid] = Instructor(cwid, name, department)

    def grade_file(self, path):
        """This method reads the grades text file and records the information about the course and grade
        of student in one dictionary and adds courses taught by the instructor in another dictionary"""

        for stu_cwid, course, grade, inst_cwid in file_reader(path, num_of_field=4, sep='\t', header=False):
            self.cwid_student[stu_cwid].add_grade(course, grade)
            self.cwid_instructor[inst_cwid].add_course(course)

    def majors_file(self, path):
        """This method reads the majors text file and records the information in a dictonary"""

        for major, flag, course in file_reader(path, num_of_field=3, sep='\t', header=False):
            if major not in self.major_course:
                self.major_course[major] = Major(major)

            self.major_course[major].add_course(flag, course)

    def stu_pretty_table(self):
        """This method populates the pretty table providing the summary of the students"""

        print()
        print("Student Summary")
        print()
        pt = PrettyTable(field_names=Student.stu_pt_header)
        for student in self.cwid_student.values():
            pt.add_row(student.one_student(self.major_course[student.major]))
        print(pt)

    def inst_pretty_table(self):
        """This method populates the pretty table providing the summary of the instructors"""

        DB_file = r"C:\Users\Asdf\PycharmProjects\SSW810\HW11.db"
        db = sqlite3.connect(DB_file)
        print()
        print("Instructor Summary")
        print()
        pt = PrettyTable(field_names=Instructor.inst_pt_header)
        query = """select i.CWID, i.Name, i.Dept, g.Course, count(g.Student_CWID) as cnt
                from HW11_instructors i
                join HW11_grades g on i.CWID = g.Instructor_CWID
                group by i.CWID, i.Name, i.Dept, g.Course"""
        for row in db.execute(query):
            pt.add_row(row)
        print (pt)

    def maj_pretty_table(self):
        """This method populates the pretty table providing the summary of courses within a major"""

        print()
        print("Major Summary")
        print()
        pt = PrettyTable(field_names=Major.maj_pt_header)
        for major in self.major_course.values():
            pt.add_row(major.one_major())
        print(pt)

def main():
    """This method calls the Repository Class"""

    Repository(r"C:\Users\Asdf\Downloads")

main()
