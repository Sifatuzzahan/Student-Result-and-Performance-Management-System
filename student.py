
class Student:

    SUBJECTS = [
        "Bangla",
        "English",
        "Mathematics",
        "Science",
        "ICT"
    ]

    def __init__(self, name, student_id, marks):
        self.name = name
        self.student_id = student_id
        self.marks = marks

    def calculate_total(self):
        total = 0

        for mark in self.marks:
            total = total + mark

        return total

    def calculate_average(self):
        average = self.calculate_total() / len(self.SUBJECTS)
        return average

    def calculate_percentage(self):
        percentage = (self.calculate_total() / 500) * 100
        return percentage

    def calculate_grade(self):
        average = self.calculate_average()

        if average >= 80:
            return "A+"
        elif average >= 70:
            return "A"
        elif average >= 60:
            return "A-"
        elif average >= 50:
            return "B"
        elif average >= 40:
            return "C"
        elif average >= 33:
            return "D"
        else:
            return "F"

    def get_status(self):
        for mark in self.marks:
            if mark < 33:
                return "Fail"

        return "Pass"

    def display_report_card(self):
        report = "\n========== STUDENT REPORT CARD ==========\n"

        report += "Student Name: " + self.name + "\n"
        report += "Student ID: " + str(self.student_id) + "\n"

        report += "\n---------- Subject-wise Marks ----------\n"

        for i in range(len(self.SUBJECTS)):
            report += self.SUBJECTS[i] + ": " + str(self.marks[i]) + "\n"

        report += "\n---------- Result Summary ----------\n"

        report += "Total Marks: " + str(self.calculate_total()) + " / 500\n"
        report += "Average: " + str(round(self.calculate_average(), 2)) + "\n"
        report += "Percentage: " + str(round(self.calculate_percentage(), 2)) + "%\n"
        report += "Grade: " + self.calculate_grade() + "\n"
        report += "Status: " + self.get_status() + "\n"

        report += "=========================================="

        return report
