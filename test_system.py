
import unittest
import tempfile
import os
import csv
from contextlib import redirect_stdout
from io import StringIO

from student import Student
from result_manager import ResultManager


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(
            "Rahim",
            "ST001",
            [85, 75, 90, 80, 70]
        )

    def test_calculate_total(self):
        self.assertEqual(self.student.calculate_total(), 400)

    def test_calculate_average(self):
        self.assertEqual(self.student.calculate_average(), 80)

    def test_calculate_percentage(self):
        self.assertEqual(self.student.calculate_percentage(), 80)

    def test_calculate_grade(self):
        self.assertEqual(self.student.calculate_grade(), "A+")

    def test_student_pass_status(self):
        self.assertEqual(self.student.get_status(), "Pass")

    def test_student_fail_status(self):
        student = Student("Karim", "ST002", [80, 75, 25, 90, 70])
        self.assertEqual(student.get_status(), "Fail")

    def test_report_card(self):
        report = self.student.display_report_card()

        self.assertIn("Rahim", report)
        self.assertIn("ST001", report)
        self.assertIn("Total Marks: 400 / 500", report)
        self.assertIn("Grade: A+", report)


class TestResultManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_directory = os.getcwd()

        os.chdir(self.temp_dir.name)

        self.manager = ResultManager()

        self.student1 = Student(
            "Rahim",
            "ST001",
            [85, 75, 90, 80, 70]
        )

        self.student2 = Student(
            "Karim",
            "ST002",
            [60, 65, 70, 55, 50]
        )

        self.student3 = Student(
            "Hasan",
            "ST003",
            [90, 95, 88, 92, 85]
        )

        self.manager.add_student(self.student1)
        self.manager.add_student(self.student2)
        self.manager.add_student(self.student3)

    def tearDown(self):
        os.chdir(self.original_directory)
        self.temp_dir.cleanup()

    def test_add_student(self):
        student = Student("Nila", "ST004", [80, 80, 80, 80, 80])

        result = self.manager.add_student(student)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_all_students()), 4)

    def test_duplicate_student_id(self):
        duplicate = Student("Another Rahim", "ST001", [70, 70, 70, 70, 70])

        result = self.manager.add_student(duplicate)

        self.assertFalse(result)
        self.assertEqual(len(self.manager.get_all_students()), 3)

    def test_search_student(self):
        student = self.manager.search_student("ST001")

        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Rahim")

    def test_search_nonexistent_student(self):
        student = self.manager.search_student("ST999")

        self.assertIsNone(student)

    def test_update_student(self):
        updated_marks = [90, 90, 90, 90, 90]

        result = self.manager.update_student("ST001", updated_marks)

        self.assertTrue(result)
        self.assertEqual(
            self.manager.search_student("ST001").marks,
            updated_marks
        )

    def test_update_invalid_marks(self):
        result = self.manager.update_student(
            "ST001",
            [90, 90, 90, 90, 110]
        )

        self.assertFalse(result)

    def test_update_nonexistent_student(self):
        result = self.manager.update_student(
            "ST999",
            [80, 80, 80, 80, 80]
        )

        self.assertFalse(result)

    def test_delete_student(self):
        result = self.manager.delete_student("ST001")

        self.assertTrue(result)
        self.assertIsNone(self.manager.search_student("ST001"))

    def test_delete_nonexistent_student(self):
        result = self.manager.delete_student("ST999")

        self.assertFalse(result)

    def test_highest_scoring_student(self):
        student = self.manager.get_highest_scoring_student()

        self.assertEqual(student.student_id, "ST003")

    def test_lowest_scoring_student(self):
        student = self.manager.get_lowest_scoring_student()

        self.assertEqual(student.student_id, "ST002")

    def test_class_summary(self):
        summary = self.manager.generate_class_summary()

        self.assertEqual(summary["total_students"], 3)
        self.assertEqual(summary["pass_count"], 3)
        self.assertEqual(summary["fail_count"], 0)

        self.assertEqual(
            summary["highest_student"].student_id,
            "ST003"
        )

        self.assertEqual(
            summary["lowest_student"].student_id,
            "ST002"
        )

        self.assertIn("Bangla", summary["subject_stats"])

    def test_save_students(self):
        result = self.manager.save_students()

        self.assertTrue(result)
        self.assertTrue(os.path.exists("students.csv"))

    def test_load_students(self):
        self.manager.save_students()

        new_manager = ResultManager()
        count = new_manager.load_students()

        self.assertEqual(count, 3)
        self.assertEqual(len(new_manager.get_all_students()), 3)

        student = new_manager.search_student("ST001")

        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Rahim")
        self.assertEqual(student.marks, [85, 75, 90, 80, 70])

    def test_load_duplicate_records(self):
        with open("students.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Name", "Student ID", "Bangla",
                "English", "Mathematics", "Science", "ICT"
            ])

            writer.writerow(["Rahim", "ST001", 80, 80, 80, 80, 80])
            writer.writerow(["Karim", "ST001", 70, 70, 70, 70, 70])

        new_manager = ResultManager()
        count = new_manager.load_students()

        self.assertEqual(count, 1)


class TestEmptyResultManager(unittest.TestCase):

    def setUp(self):
        self.manager = ResultManager()

    def test_empty_highest_student(self):
        self.assertIsNone(
            self.manager.get_highest_scoring_student()
        )

    def test_empty_lowest_student(self):
        self.assertIsNone(
            self.manager.get_lowest_scoring_student()
        )

    def test_empty_class_summary(self):
        summary = self.manager.generate_class_summary()

        self.assertEqual(summary["total_students"], 0)
        self.assertEqual(summary["pass_count"], 0)
        self.assertEqual(summary["fail_count"], 0)
        self.assertEqual(summary["pass_percentage"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
