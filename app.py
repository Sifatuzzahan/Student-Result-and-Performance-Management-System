
import os

from student import Student
from result_manager import ResultManager

# ============================================================
# SYSTEM INITIALIZATION
# ============================================================

subjects = Student.SUBJECTS

result_manager = ResultManager()

loaded_count = result_manager.load_students()

# ============================================================
# TERMINAL UI UTILITIES
# ============================================================

WIDTH = 75

def clear_screen():
    """Clear terminal screen."""

    os.system("cls" if os.name == "nt" else "clear")

def print_line(char="=", width=WIDTH):
    print(char * width)

def print_header(title):

    print()
    print_line("=")
    print(title.center(WIDTH))
    print_line("=")

def print_message(message, message_type="info"):

    if message_type == "success":
        label = "[SUCCESS]"

    elif message_type == "error":
        label = "[ERROR]"

    elif message_type == "warning":
        label = "[WARNING]"

    else:
        label = "[INFO]"

    print()
    print(f"  {label} {message}")

def pause_screen():

    print()
    input("  Press Enter to continue...")

def get_valid_string(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print_message(
                "This field cannot be empty.",
                "error"
            )

        else:
            return value

def get_valid_mark(subject):

    while True:

        try:

            mark = int(
                input(
                    f"Enter {subject} Marks (0-100): "
                )
            )

            if 0 <= mark <= 100:
                return mark

            print_message(
                "Enter marks between 0 and 100.",
                "warning"
            )

        except ValueError:

            print_message(
                "Please enter a valid number.",
                "error"
            )

# ============================================================
# PROFESSIONAL BOX-STYLE STUDENT TABLE
# ============================================================

def display_student_table(students):

    if len(students) == 0:

        print_message(
            "No student records found.",
            "warning"
        )
        return

    # Column widths
    widths = [18, 12, 9, 10, 8, 8]

    # Create table border
    border = (
        "+"
        + "+".join("-" * width for width in widths)
        + "+"
    )

    # Table headers
    headers = [
        "Student Name",
        "Student ID",
        "Total",
        "Average",
        "Grade",
        "Status"
    ]

    print()
    print(border)

    print(
        "|"
        + "|".join(
            f"{headers[i]:^{widths[i]}}"
            for i in range(len(headers))
        )
        + "|"
    )

    print(border)

    # Display student records
    for student in students:

        values = [
            student.name[:17],
            str(student.student_id)[:11],
            str(student.calculate_total()),
            f"{student.calculate_average():.2f}",
            student.calculate_grade(),
            student.get_status().upper()
        ]

        print(
            "|"
            + "|".join(
                f"{values[i]:^{widths[i]}}"
                for i in range(len(values))
            )
            + "|"
        )

    print(border)

    print()
    print(f"  Total Student Records: {len(students)}")

# ============================================================
# PROFESSIONAL DASHBOARD
# ============================================================

def print_dashboard():

    summary = result_manager.generate_class_summary()

    print()

    print("+" + "=" * 73 + "+")
    print(
        "|"
        + " STUDENT RESULT MANAGEMENT SYSTEM ".center(73)
        + "|"
    )
    print(
        "|"
        + " PROFESSIONAL DASHBOARD ".center(73)
        + "|"
    )
    print("+" + "=" * 73 + "+")

    print("\n  SYSTEM OVERVIEW")
    print("  " + "-" * 69)

    print(
        f"  {'Total Students':<21}: "
        f"{summary['total_students']}"
    )

    print(
        f"  {'Passed Students':<21}: "
        f"{summary['pass_count']}"
    )

    print(
        f"  {'Failed Students':<21}: "
        f"{summary['fail_count']}"
    )

    print(
        f"  {'Pass Percentage':<21}: "
        f"{summary['pass_percentage']}%"
    )

    print(
        f"  {'Fail Percentage':<21}: "
        f"{summary['fail_percentage']}%"
    )

    print(
        f"  {'Class Average':<21}: "
        f"{summary['class_average_percentage']}%"
    )

    print("\n  CLASS PERFORMANCE")
    print("  " + "-" * 69)

    highest = summary["highest_student"]
    lowest = summary["lowest_student"]

    if highest is not None:

        print(
            f"  {'Top Performer':<21}: "
            f"{highest.name} (ID: {highest.student_id})"
        )

        print(
            f"  {'Highest Total':<21}: "
            f"{highest.calculate_total()}/500"
        )

        print(
            f"  {'Lowest Performer':<21}: "
            f"{lowest.name} (ID: {lowest.student_id})"
        )

        print(
            f"  {'Lowest Total':<21}: "
            f"{lowest.calculate_total()}/500"
        )

    else:

        print("  No student records available.")

    print("\n  " + "=" * 69)

    print(
        "  Welcome! Manage your student records efficiently."
    )

    print("+" + "=" * 73 + "+")

# ============================================================
# STUDENT MANAGEMENT
# ============================================================

def add_student():

    print_header("ADD NEW STUDENT")

    name = get_valid_string("Enter Student Name: ")

    student_id = get_valid_string("Enter Student ID: ")

    if result_manager.search_student(student_id) is not None:

        print_message(
            "This Student ID already exists!",
            "error"
        )
        return

    marks = []

    print("\nEnter Subject-wise Marks")
    print("-" * 40)

    for subject in subjects:

        mark = get_valid_mark(subject)
        marks.append(mark)

    student = Student(name, student_id, marks)

    if result_manager.add_student(student):

        print_message(
            "Student added successfully!",
            "success"
        )

        result_manager.save_students()

        print(student.display_report_card())

def display_all_students():

    print_header("ALL STUDENT RECORDS")

    students = result_manager.get_all_students()

    display_student_table(students)

def show_student_performance():

    print_header("STUDENT PERFORMANCE OVERVIEW")

    students = result_manager.get_all_students()

    display_student_table(students)

def search_student():

    print_header("SEARCH STUDENT")

    student_id = get_valid_string("Enter Student ID: ")

    student = result_manager.search_student(student_id)

    if student is not None:

        print_message(
            "Student record found.",
            "success"
        )

        print(student.display_report_card())

    else:

        print_message(
            "Student not found!",
            "error"
        )

def show_highest_student():

    print_header("HIGHEST SCORING STUDENT")

    student = result_manager.get_highest_scoring_student()

    if student is None:

        print_message(
            "No student records found.",
            "warning"
        )

    else:

        print(student.display_report_card())

def show_lowest_student():

    print_header("LOWEST SCORING STUDENT")

    student = result_manager.get_lowest_scoring_student()

    if student is None:

        print_message(
            "No student records found.",
            "warning"
        )

    else:

        print(student.display_report_card())

# ============================================================
# CLASS PERFORMANCE SUMMARY
# ============================================================

def show_class_summary():

    print_header("CLASS PERFORMANCE SUMMARY")

    summary = result_manager.generate_class_summary()

    if summary["total_students"] == 0:

        print_message(
            "No student records found.",
            "warning"
        )
        return

    print("\nGENERAL STATISTICS")
    print("-" * 50)

    print("Total Students:", summary["total_students"])
    print("Passed Students:", summary["pass_count"])
    print("Failed Students:", summary["fail_count"])

    print("Pass Percentage:", summary["pass_percentage"], "%")
    print("Fail Percentage:", summary["fail_percentage"], "%")

    print(
        "Class Average Percentage:",
        summary["class_average_percentage"],
        "%"
    )

    highest = summary["highest_student"]
    lowest = summary["lowest_student"]

    print("\nTOP AND LOWEST PERFORMERS")
    print("-" * 50)

    print(
        "Highest Scoring Student:",
        highest.name,
        "| ID:", highest.student_id,
        "| Total:", highest.calculate_total()
    )

    print(
        "Lowest Scoring Student:",
        lowest.name,
        "| ID:", lowest.student_id,
        "| Total:", lowest.calculate_total()
    )

    print("\nGRADE DISTRIBUTION")
    print("-" * 50)

    print(
        f"{'Grade':<12}"
        f"{'Students':<12}"
        f"Distribution"
    )

    print("-" * 45)

    for grade, count in summary["grade_counts"].items():

        percentage = (
            count / summary["total_students"]
        ) * 100

        print(
            f"{grade:<12}"
            f"{count:<12}"
            f"{'#' * count} ({percentage:.1f}%)"
        )

    print("\nSUBJECT-WISE PERFORMANCE")
    print("-" * 54)

    print(
        f"{'Subject':<18}"
        f"{'Average':<12}"
        f"{'Highest':<12}"
        f"{'Lowest':<12}"
    )

    print("-" * 54)

    for subject, stats in summary["subject_stats"].items():

        print(
            f"{subject:<18}"
            f"{stats['average']:<12.2f}"
            f"{stats['highest']:<12}"
            f"{stats['lowest']:<12}"
        )

    print("-" * 54)

    print("\nINDIVIDUAL STUDENT PERFORMANCE")

    display_student_table(
        result_manager.get_all_students()
    )

# ============================================================
# UPDATE STUDENT
# ============================================================

def update_student():

    print_header("UPDATE STUDENT MARKS")

    student_id = get_valid_string("Enter Student ID: ")

    student = result_manager.search_student(student_id)

    if student is None:

        print_message(
            "Student not found!",
            "error"
        )
        return

    print("\nUpdating Marks for:", student.name)

    print("Press Enter to keep existing marks.")

    updated_marks = []

    for i in range(len(subjects)):

        current_mark = student.marks[i]

        while True:

            raw_mark = input(
                subjects[i]
                + " [Current: "
                + str(current_mark)
                + "]: "
            ).strip()

            if raw_mark == "":

                updated_marks.append(current_mark)
                break

            try:

                new_mark = int(raw_mark)

                if 0 <= new_mark <= 100:

                    updated_marks.append(new_mark)
                    break

                print_message(
                    "Marks must be between 0 and 100.",
                    "warning"
                )

            except ValueError:

                print_message(
                    "Please enter a valid number.",
                    "error"
                )

    if result_manager.update_student(
        student_id,
        updated_marks
    ):

        print_message(
            "Student marks updated successfully!",
            "success"
        )

        print(student.display_report_card())

    else:

        print_message(
            "Unable to update student marks!",
            "error"
        )

# ============================================================
# DELETE STUDENT
# ============================================================

def delete_student():

    print_header("DELETE STUDENT")

    student_id = get_valid_string("Enter Student ID: ")

    student = result_manager.search_student(student_id)

    if student is None:

        print_message(
            "Student not found!",
            "error"
        )
        return

    print("\nStudent Name:", student.name)
    print("Student ID:", student.student_id)

    confirmation = input(
        "\nAre you sure you want to delete? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        if result_manager.delete_student(student_id):

            print_message(
                "Student deleted successfully!",
                "success"
            )

        else:

            print_message(
                "Unable to delete student!",
                "error"
            )

    else:

        print_message(
            "Deletion cancelled.",
            "warning"
        )

# ============================================================
# DATA MANAGEMENT
# ============================================================

def reload_students():

    print_header("RELOAD STUDENT DATA")

    count = result_manager.load_students()

    print_message(
        f"{count} student records loaded.",
        "success"
    )

    print("\nLoaded Student Performance:")

    show_student_performance()

def save_student_data():

    print_header("SAVE STUDENT DATA")

    if result_manager.save_students():

        print_message(
            "All student records saved successfully!",
            "success"
        )

    else:

        print_message(
            "Unable to save student records!",
            "error"
        )

# ============================================================
# PROFESSIONAL NAVIGATION MENU
# ============================================================

def display_menu():

    print_header(
        "STUDENT RESULT & PERFORMANCE MANAGEMENT SYSTEM"
    )

    print("\n  STUDENT MANAGEMENT")
    print("  " + "-" * 69)

    print("  [01] Add New Student")
    print("  [02] View All Students")
    print("  [03] Search Student by ID")

    print("\n  PERFORMANCE ANALYSIS")
    print("  " + "-" * 69)

    print("  [04] Show Highest Scoring Student")
    print("  [05] Show Lowest Scoring Student")
    print("  [06] Class Performance Summary")

    print("\n  RECORD MANAGEMENT")
    print("  " + "-" * 69)

    print("  [07] Update Student Marks")
    print("  [08] Delete Student")
    print("  [09] Reload Data & View Performance")
    print("  [10] Save Data to CSV")

    print("\n  SYSTEM")
    print("  " + "-" * 69)

    print("  [00] Exit")

    print()
    print_line("=")

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    clear_screen()

    print_dashboard()

    print(
        f"\n  Previously Loaded Students: {loaded_count}"
    )

    pause_screen()

    while True:

        clear_screen()

        display_menu()

        choice = input(
            "\n  Enter Your Choice: "
        ).strip()

        if choice == "1":

            clear_screen()
            add_student()
            pause_screen()

        elif choice == "2":

            clear_screen()
            display_all_students()
            pause_screen()

        elif choice == "3":

            clear_screen()
            search_student()
            pause_screen()

        elif choice == "4":

            clear_screen()
            show_highest_student()
            pause_screen()

        elif choice == "5":

            clear_screen()
            show_lowest_student()
            pause_screen()

        elif choice == "6":

            clear_screen()
            show_class_summary()
            pause_screen()

        elif choice == "7":

            clear_screen()
            update_student()
            pause_screen()

        elif choice == "8":

            clear_screen()
            delete_student()
            pause_screen()

        elif choice == "9":

            clear_screen()
            reload_students()
            pause_screen()

        elif choice == "10":

            clear_screen()
            save_student_data()
            pause_screen()

        elif choice == "0":

            clear_screen()

            print_header("EXIT APPLICATION")

            print("\nSaving student records...")

            if result_manager.save_students():

                print_message(
                    "All student data has been saved.",
                    "success"
                )

                print(
                    "\nThank you for using "
                    "Student Result Management System!"
                )

            else:

                print_message(
                    "Unable to save student data.",
                    "error"
                )

            break

        else:

            print_message(
                "Invalid choice! Please select a valid option.",
                "error"
            )

            pause_screen()

# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()