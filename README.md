# Student Result and Performance Management System

A Python-based terminal application designed to manage student records, calculate academic results, and analyze class performance.

## Project Overview

The Student Result and Performance Management System is a menu-driven application developed using Python and Object-Oriented Programming (OOP).

It provides a simple way to manage student information, record subject-wise marks, calculate academic results, and generate class performance statistics.

Student records are stored in a CSV file so that data can be saved and loaded between application sessions.

## Key Features

### Student Management
- Add new student records
- Prevent duplicate Student IDs
- Search students by Student ID
- Display all student records
- Update student marks
- Delete student records

### Result Management
- Calculate total marks
- Calculate average marks
- Calculate percentage
- Automatically assign grades
- Determine Pass or Fail status
- Generate individual student report cards

### Performance Analysis
- Identify the highest-scoring student
- Identify the lowest-scoring student
- Generate class performance summaries
- Display pass and fail statistics
- Show grade distribution
- Calculate subject-wise average, highest, and lowest marks

### Data Management
- Save student records in CSV format
- Load previously saved records
- Reload student data
- Validate student marks

## Subjects and Grading System

The system manages five subjects:

1. Bangla
2. English
3. Mathematics
4. Science
5. ICT

**Total Marks:** 500

**Passing Criteria:** A student must obtain at least 33 marks in every subject to pass.

### Grading Scale

| Average Marks | Grade |
|---|---|
| 80–100 | A+ |
| 70–79 | A |
| 60–69 | A- |
| 50–59 | B |
| 40–49 | C |
| 33–39 | D |
| Below 33 | F |

## Technologies Used

- Python 3
- CSV Module
- Object-Oriented Programming (OOP)
- unittest Framework
- Terminal / Command-Line Interface

## Project Structure

```text
Student_Result_and_Performance_Management_System/
│
├── app.py
├── student.py
├── result_manager.py
├── test_system.py
├── students.csv
├── README.md
│
└── screenshots/
    ├── 01_dashboard.png
    ├── 02_main_menu.png
    ├── 03_student_records.png
    ├── 04_class_summary.png
    ├── 05_update_student.png
    └── 06_search_student.png
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd Student_Result_and_Performance_Management_System
```

### 3. Run the Application

```bash
python app.py
```

## Running Tests

The project includes an automated test suite built with Python's built-in `unittest` framework.

To run the tests:

```bash
python test_system.py
```

## Data Storage

Student information is stored in `students.csv`.

The application uses CSV file handling to save and load student records.

## Screenshots

The `screenshots/` directory contains screenshots of the application's dashboard, navigation menu, student records, class summary, update feature, and search feature.

## Author

**Sifatuzzahan**

## License

This project is developed for educational purposes.