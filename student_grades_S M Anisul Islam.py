import json
import os

# -------------------------------
# Load student data from JSON if available
# -------------------------------
def load_data(filename="students.json"):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"✅ Loaded student data from '{filename}'.")
            return data
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
    # If no file exists, return default initial data
    return {
        "S001": {
            "name": "Alice Johnson",
            "age": 20,
            "school_name": "Tech University",
            "completed_courses": {"Math101": 88, "CS201": 95, "History101": 79},
            "ongoing_courses": {"Physics202": "A", "Art105": "In Progress"}
        },
        "S002": {
            "name": "Bob Smith",
            "age": 21,
            "school_name": "State College",
            "completed_courses": {"Math101": 92, "Literature301": 85, "Philosophy101": 90},
            "ongoing_courses": {"Chemistry200": 75, "Sociology305": "In Progress"}
        },
        "S003": {
            "name": "Charlie Brown",
            "age": 19,
            "school_name": "Tech University",
            "completed_courses": {"CS201": 75, "Economics302": 82},
            "ongoing_courses": {"Biology101": 90}
        }
    }

students_data = load_data()

# -------------------------------
# Menu display
# -------------------------------
def display_menu():
    print("\n" + "="*50)
    print("🎓 Student Grades Management System 📝")
    print("="*50)
    print("1. View all students' information")
    print("2. View specific student information")
    print("3. View ongoing grades of a student")
    print("4. View completed grades of a student")
    print("5. View average completed grades of a student")
    print("6. View a specific grade of a student")
    print("7. Add a new student")
    print("8. Add a course to an existing student")
    print("9. Save student data to JSON file")
    print("10. Exit")
    print("="*50)

# -------------------------------
# Helper functions (same as before)
# -------------------------------
def get_student_id(prompt="Enter student ID: "):
    student_id = input(prompt).strip().upper()
    if student_id not in students_data:
        print(f"❌ Error: Student with ID '{student_id}' does not exist.")
        return None
    return student_id

def view_all_students(data):
    print("\n--- All Students ---")
    for sid, info in data.items():
        print(f"ID: {sid}, Name: {info['name']}, Age: {info['age']}, School: {info['school_name']}")
        print(f"  Completed Courses: {len(info['completed_courses'])}, Ongoing Courses: {len(info['ongoing_courses'])}")
    print("------------------")

def view_specific_student(data):
    sid = get_student_id()
    if sid:
        info = data[sid]
        print(f"\nID: {sid}\nName: {info['name']}\nAge: {info['age']}\nSchool: {info['school_name']}")
        print("Completed Courses & Grades:")
        for course, grade in info['completed_courses'].items():
            print(f"  - {course}: {grade}")
        print("Ongoing Courses & Grades/Status:")
        for course, grade in info['ongoing_courses'].items():
            print(f"  - {course}: {grade}")

def view_ongoing_grades(data):
    sid = get_student_id()
    if sid:
        ongoing = data[sid]['ongoing_courses']
        print(f"\nOngoing Courses for {data[sid]['name']} (ID: {sid}):")
        for course, grade in ongoing.items():
            print(f"  - {course}: {grade}")

def view_completed_grades(data):
    sid = get_student_id()
    if sid:
        completed = data[sid]['completed_courses']
        print(f"\nCompleted Courses for {data[sid]['name']} (ID: {sid}):")
        for course, grade in completed.items():
            print(f"  - {course}: {grade}")

def view_average_completed_grades(data):
    sid = get_student_id()
    if sid:
        completed = data[sid]['completed_courses']
        numeric_grades = [g for g in completed.values() if isinstance(g, (int, float))]
        if numeric_grades:
            avg = sum(numeric_grades) / len(numeric_grades)
            print(f"\nAverage completed grade for {data[sid]['name']} (ID: {sid}): {avg:.2f}")
        else:
            print(f"No numerical completed grades for {data[sid]['name']}.")

def view_specific_grade(data):
    sid = get_student_id()
    if sid:
        course_name = input("Enter the course name: ").strip()
        info = data[sid]
        grade = None
        course_type = ""
        if course_name in info['completed_courses']:
            grade = info['completed_courses'][course_name]
            course_type = "Completed"
        elif course_name in info['ongoing_courses']:
            grade = info['ongoing_courses'][course_name]
            course_type = "Ongoing"
        if grade is not None:
            print(f"Grade for {course_name} ({course_type}) for {info['name']} (ID: {sid}): {grade}")
        else:
            print(f"❌ Course '{course_name}' not found for student ID '{sid}'.")

# -------------------------------
# New features
# -------------------------------
def add_new_student(data):
    sid = input("Enter new student ID (e.g., S004): ").strip().upper()
    if sid in data:
        print("❌ Student ID already exists.")
        return
    name = input("Enter student name: ").strip()
    while True:
        age = input("Enter age: ").strip()
        if age.isdigit():
            age = int(age)
            break
        print("❌ Please enter a valid number for age.")
    school = input("Enter school name: ").strip()
    data[sid] = {"name": name, "age": age, "school_name": school, "completed_courses": {}, "ongoing_courses": {}}
    print(f"✅ Student '{name}' added successfully with ID '{sid}'.")

def add_course_to_student(data):
    sid = get_student_id()
    if not sid:
        return
    course_name = input("Enter course name: ").strip()
    while True:
        course_type = input("Is it completed or ongoing? (c/o): ").strip().lower()
        if course_type in ['c', 'o']:
            break
        print("❌ Enter 'c' for completed or 'o' for ongoing.")
    grade = input("Enter grade or status: ").strip()
    if course_type == 'c':
        try:
            grade_val = float(grade)
        except ValueError:
            grade_val = grade  # Allow letter grades
        data[sid]['completed_courses'][course_name] = grade_val
    elif course_type == 'o':
        data[sid]['ongoing_courses'][course_name] = grade
    print(f"✅ Course '{course_name}' added to student '{data[sid]['name']}'.")

def save_to_json(data):
    filename = input("Enter JSON filename to save (e.g., students.json): ").strip()
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# -------------------------------
# Main program loop
# -------------------------------
def main():
    running = True
    while running:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            view_all_students(students_data)
        elif choice == '2':
            view_specific_student(students_data)
        elif choice == '3':
            view_ongoing_grades(students_data)
        elif choice == '4':
            view_completed_grades(students_data)
        elif choice == '5':
            view_average_completed_grades(students_data)
        elif choice == '6':
            view_specific_grade(students_data)
        elif choice == '7':
            add_new_student(students_data)
        elif choice == '8':
            add_course_to_student(students_data)
        elif choice == '9':
            save_to_json(students_data)
        elif choice == '10':
            print("👋 Exiting program. Goodbye!")
            running = False
        else:
            print("⚠️ Invalid choice. Please enter 1-10.")

        if running:
            another = input("\nPerform another operation? (yes/no): ").strip().lower()
            if another not in ['yes', 'y']:
                print("👋 Exiting program. Goodbye!")
                running = False

if __name__ == "__main__":
    main()
