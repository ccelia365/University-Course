import unittest
import os
from University import Repository

class TestUniversity(unittest.TestCase):
    """This test class tests the methods within University"""

    def test_one_student(self):
        """This method tests the summary of students"""

        my_rep = Repository (r"C:\Users\Asdf\Downloads")

        expect = [["10103", "Baldwin, C", "SFEN", ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                  ["11714", "Morton, A", "SYEN", ['SYS 611', 'SYS 645']],
                  ["11461", "Wright, U", "SYEN", ['SYS 611', 'SYS 750', 'SYS 800'] ],
                  ["11788", "Fuller, E", "SYEN", ['SSW 540'] ],
                  ["10175", "Erickson, D", "SFEN", ['SSW 564', 'SSW 567', 'SSW 687'] ],
                  ["10183", "Chapman, O", "SFEN", ['SSW 689']],
                  ["10172", "Forbes, I", "SFEN", ['SSW 555', 'SSW 567']],
                  ["11399", "Cordova, I", "SYEN", ['SSW 540']],
                  ["10115", "Wyatt, X", "SFEN", ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'] ],
                  ["11658", "Kelly, P", "SYEN", ['SSW 540'] ]]

        students = [student.one_student() for student in my_rep.cwid_student.values()]

        self.assertEqual(sorted(expect), sorted(students))

    def test_one_instructor(self):
        """This method tests the summary of teachers"""

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

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
