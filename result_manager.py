
import csv

from student import Student


class ResultManager:

    def __init__(self):
        self.students = []

    # Add a new student
    def add_student(self, student):
        existing_student = self.search_student(student.student_id)

        if existing_student is not None:
            print("This Student ID Already Exists!")
            return False

        self.students.append(student)
        return True

    # Get all students
    def get_all_students(self):
        return self.students

    # Search student by ID
    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student

        return None

    # Update student marks
    def update_student(self, student_id, updated_marks):
        student = self.search_student(student_id)

        if student is None:
            return False

        if len(updated_marks) != 5:
            return False

        for mark in updated_marks:
            if mark < 0 or mark > 100:
                return False

        student.marks = updated_marks
        self.save_students()

        return True

    # Delete student
    def delete_student(self, student_id):
        student = self.search_student(student_id)

        if student is None:
            return False

        self.students.remove(student)
        self.save_students()

        return True

    # Find highest scoring student
    def get_highest_scoring_student(self):
        if len(self.students) == 0:
            return None

        highest_student = self.students[0]

        for student in self.students:
            if student.calculate_total() > highest_student.calculate_total():
                highest_student = student

        return highest_student

    # Find lowest scoring student
    def get_lowest_scoring_student(self):
        if len(self.students) == 0:
            return None

        lowest_student = self.students[0]

        for student in self.students:
            if student.calculate_total() < lowest_student.calculate_total():
                lowest_student = student

        return lowest_student

    # Generate class performance summary
    def generate_class_summary(self):
        total_students = len(self.students)

        passed_students = 0
        failed_students = 0

        grade_counts = {
            "A+": 0,
            "A": 0,
            "A-": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0
        }

        total_percentage = 0

        for student in self.students:

            if student.get_status() == "Pass":
                passed_students = passed_students + 1
            else:
                failed_students = failed_students + 1

            grade = student.calculate_grade()
            grade_counts[grade] = grade_counts[grade] + 1

            total_percentage = total_percentage + student.calculate_percentage()

        if total_students > 0:
            pass_percentage = round((passed_students / total_students) * 100, 2)
            fail_percentage = round((failed_students / total_students) * 100, 2)
            class_average_percentage = round(total_percentage / total_students, 2)
        else:
            pass_percentage = 0
            fail_percentage = 0
            class_average_percentage = 0

        # Subject-wise performance
        subject_stats = {}

        for i in range(len(Student.SUBJECTS)):

            subject = Student.SUBJECTS[i]
            marks_list = []

            for student in self.students:
                marks_list.append(student.marks[i])

            if len(marks_list) > 0:
                subject_average = sum(marks_list) / len(marks_list)
                subject_highest = max(marks_list)
                subject_lowest = min(marks_list)
            else:
                subject_average = 0
                subject_highest = 0
                subject_lowest = 0

            subject_stats[subject] = {
                "average": round(subject_average, 2),
                "highest": subject_highest,
                "lowest": subject_lowest
            }

        return {
            "total_students": total_students,
            "pass_count": passed_students,
            "fail_count": failed_students,
            "pass_percentage": pass_percentage,
            "fail_percentage": fail_percentage,
            "class_average_percentage": class_average_percentage,
            "highest_student": self.get_highest_scoring_student(),
            "lowest_student": self.get_lowest_scoring_student(),
            "grade_counts": grade_counts,
            "subject_stats": subject_stats
        }

    # Save student data to CSV
    def save_students(self):
        try:
            with open("students.csv", "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Name", "Student ID", "Bangla",
                    "English", "Mathematics", "Science", "ICT"
                ])

                for student in self.students:
                    writer.writerow([
                        student.name,
                        student.student_id,
                        student.marks[0],
                        student.marks[1],
                        student.marks[2],
                        student.marks[3],
                        student.marks[4]
                    ])

            print("Student Data Saved Successfully!")
            return True

        except OSError:
            print("Error! Unable to Save Student Data.")
            return False

    # Load student data from CSV
    def load_students(self):
        self.students = []

        try:
            with open("students.csv", "r", newline="") as file:
                reader = csv.reader(file)

                header = next(reader, None)

                if header is None:
                    return 0

                for row in reader:

                    if len(row) != 7:
                        continue

                    name = row[0].strip()
                    student_id = row[1].strip()

                    if name == "" or student_id == "":
                        continue

                    try:
                        marks = []

                        for i in range(2, 7):
                            mark = int(row[i])

                            if mark < 0 or mark > 100:
                                raise ValueError

                            marks.append(mark)

                    except ValueError:
                        continue

                    if self.search_student(student_id) is not None:
                        continue

                    student = Student(name, student_id, marks)
                    self.students.append(student)

            return len(self.students)

        except FileNotFoundError:
            print("CSV File Not Found!")
            return 0

        except OSError:
            print("Error! Unable to Read CSV File.")
            return 0
