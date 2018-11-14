import unittest
import os
from University import Repository

class TestUniversity2(unittest.TestCase):
    """This class tests the summary of students, instructors and majors"""

    def test_one_student(self):
        """This method tests the summary of students """

        my_rep = Repository (r"C:\Users\Asdf\Downloads")

        expect = [["10103", "Baldwin, C", "SFEN", ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'],
                   {'SSW 540', 'SSW 555'},None],

                  ["11788", "Fuller, E", "SYEN", ['SSW 540'], {'SYS 671', 'SYS 800', 'SYS 612'}, None],

                  ["10172", "Forbes, I", "SFEN", ['SSW 555', 'SSW 567'], {'SSW 540', 'SSW 564'}, {'CS 501', 'CS 545', 'CS 513'}],

                  ["10175", "Erickson, D", "SFEN",['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'},
                   {'CS 501', 'CS 545', 'CS 513'}],

                  ["10115", "Wyatt, X", "SFEN", ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, None],

                  ["11399", "Cordova, I", "SYEN", ['SSW 540'], {'SYS 671', 'SYS 800', 'SYS 612'}, None],

                  ["11714", "Morton, A", "SYEN", ['SYS 611', 'SYS 645'], {'SYS 671', 'SYS 800', 'SYS 612'},
                   {'SSW 810', 'SSW 565', 'SSW 540'}],

                  ["11658", "Kelly, P", "SYEN", [], {'SYS 671', 'SYS 800', 'SYS 612'}, {'SSW 810', 'SSW 565', 'SSW 540'}],

                  ["10183", "Chapman, O", "SFEN", ['SSW 689'], {'SSW 540', 'SSW 555', 'SSW 567', 'SSW 564'},
                   {'CS 501', 'CS 545', 'CS 513'}],

                  ["11461", "Wright, U", "SYEN", ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 671', 'SYS 612'},
                   {'SSW 810', 'SSW 565', 'SSW 540'}] ]

        students = [student.one_student(my_rep.major_course[student.major]) for student in my_rep.cwid_student.values()]

        self.assertEqual(sorted(expect), sorted(students))

    def test_one_instructor(self):
        """This method tests the summary of instructors"""

        my_rep = Repository (r"C:\Users\Asdf\Downloads")

        expect = [["98765", "Einstein, A", "SFEN", "SSW 540", 3],
                  ["98765", "Einstein, A", "SFEN", "SSW 567", 4],
                  ["98760", "Darwin, C", "SYEN", "SYS 645", 1],
                  ["98760", "Darwin, C", "SYEN", "SYS 800", 1],
                  ["98760", "Darwin, C", "SYEN", "SYS 750", 1],
                  ["98760", "Darwin, C", "SYEN", "SYS 611", 2],
                  ["98764", "Feynman, R", "SFEN", "SSW 564", 3],
                  ["98764", "Feynman, R", "SFEN", "SSW 687", 3],
                  ["98764", "Feynman, R", "SFEN", "CS 545", 1],
                  ["98764", "Feynman, R", "SFEN", "CS 501", 1],
                  ["98763", "Newton, I", "SFEN", "SSW 689", 1],
                  ["98763", "Newton, I", "SFEN", "SSW 555", 1]]

        instructors = [course for instructor in my_rep.cwid_instructor.values() for course in instructor.one_instructor()]

        self.assertEqual(sorted(expect), sorted(instructors))

    def test_one_major(self):
        """This method tests the summary of majors"""

        my_rep = Repository (r"C:\Users\Asdf\Downloads")

        expect = [["SFEN", ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                  ["SYEN", ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]

        majors = [major.one_major() for major in my_rep.major_course.values()]

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
