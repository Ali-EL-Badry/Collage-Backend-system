import sqlite3

db = sqlite3.connect("competition.db")
cr = db.cursor()


def gpa_grade_check(limit, text):
    while True:
        try:
            grade_gpa = int(input(f"Enter Student {text} :"))
            if grade_gpa < 5 and int(grade_gpa) >= limit:
                return grade_gpa
            else:
                print(f"Please enter a right {text}")
        except ValueError:
            print(f"Please enter a right {text}")


# to make the yes and no functions
def continue_or(what):
    menu = f'''Do you want to {what} ?
[A] Yes
[B] No
Choose (A/B):'''
    option = ['A', 'B']
    if check(menu, option) == 'A':
        return True
    else:
        return False


# to check the right input
def check(text, choices_type):
    while True:
        option = input(text).upper()
        print("====================================")
        if option in choices_type:
            return option
        else:
            print('please enter a right input')


# to check the existence of id
def check_get_id():
    cr.execute("SELECT id FROM students")
    all_ids = cr.fetchall()
    while True:
        iD = input("Enter student ID you want: ")
        if (iD,) in all_ids:
            return iD
        else:
            print("This ID is not found. Try again.")


def showing_courses():
    cr.execute(f"select course from course_for_student where id = '{student_id}'")
    courses_of_student = cr.fetchall()
    print("Courses that you have not registered:", end=" ")
    for l in list_of_coursesA:
        if l not in courses_of_student:
            print(l[0], end=", ")

    print("\nCourses that you have registered:", end=" ")
    if courses_of_student:
        for j in courses_of_student:
            if j is not courses_of_student[len(courses_of_student)-1]:
                print(j[0], end=", ")
        print(courses_of_student[len(courses_of_student)-1][0])
    else:
        print("No courses")


def register_courses(student_id):
    while True:
        showing_courses()
        print("===================================================")
        rc = input("Please Write The Courses You Want Register: ")
        cr.execute(f"select course from course_for_student where course = '{rc}' and id = '{student_id}'")
        saved_c = cr.fetchone()
        if saved_c is None:
            if (rc,) in list_of_coursesA:
                cr.execute("insert into course_for_student(id, course) values(?, ?)", (student_id, rc))
                print("===========================================")
                print(f"== {rc} is added successfully! ==")
                print("===========================================")

                db.commit()
                if not continue_or("register other courses"):
                    break
            else:
                print("Invalid input")
        else:
            print("The course already exists")


# edit courses
def edit_courses():
    cr.execute(f"select * from course_for_student where id = '{student_id}'")
    list_of_coursesS = cr.fetchall()
    if not list_of_coursesS:
        print("Doesn't exist courses to edit")
    else:
        while True:
            while True:
                showing_courses()
                old_course = input("Please Write course that you have registered: ")
                if (student_id, old_course) not in list_of_coursesS:
                    print("Please enter an assigned course")
                    print("===============================")
                else:
                    break

            print("===========================================================")
            menuE = "What do you want to do?\n[D] Delete the course \n[U] Update the course \nYour choice: "
            optionE = ['D', 'U']
            choiceE = check(menuE, optionE)
            if choiceE == "U":
                while True:
                    new_course = input("Please write the new course: ")
                    if (new_course,) in list_of_coursesA:
                        cr.execute("update course_for_student set course = ? where course = ? and id = ?",
                                   (new_course, old_course, student_id))

                        print("=======================================")
                        print(f"The {old_course} is updated successfully!")
                        print("=======================================")
                        break
                    else:
                        print("Invalid input")

            elif choiceE == "D":
                cr.execute("delete from course_for_student where course = ? and id = ?",
                           (old_course, student_id))
                print("===================================")
                print(f"The {old_course} is deleted successfully!")
                print("===================================")

            if not continue_or("make another edit"):
                break


# choosing group
def chosen_group():
    while True:
        cr.execute(f"select group_type from students where id = '{student_id}'")
        saved_g = cr.fetchone()
        if saved_g[0] is None:
            cg = input("Please Write the The Group You Want to Choose (A/B): ").upper()
            if cg == "A" or cg == "B":
                cr.execute("update students set group_type = ? where id = ?", (cg, student_id))
                print("==================================")
                print("The group is updated successfully!")
                print("==================================")

                break
            else:
                print("Invalid input")
                print("=========================================================")
        else:
            print("You had chosen the group already")
            print("=================================")
            break


# Begin of the program
print('===Welcome To College Management System===')

# Menu 1
menu1 = "Define your Carrier\n[A] Control Member\n[B] Student\n[C] Exit\nChoose (A/B/C): "
option1 = ['A', 'B', 'C']
choice = check(menu1, option1)

# Control Part
if choice == 'A':
    cr.execute("SELECT name FROM admin")
    names = cr.fetchall()
    cr.execute("SELECT password FROM admin")
    passwords = cr.fetchall()

    print("====Control Member===")

    # Check of the admin access
    while True:
        name_control = input("Enter your Name: ")
        password_control = input("please enter your Password: ")
        print("====================================")
        if (name_control,) in names and (password_control,) in passwords:
            print(f"Welcome Mr|{name_control}")
            break
        else:
            print("This name or password are not found. Try again.")

    # Menu 2
    while True:
        menu2 = '''Which function do you want to do?
[A] Add Student
[B] Remove Student
[C] Modify Student Data
[D] Add Course 
[E] Remove Course
[F] See all information of a student
[G] List of all Students
[H] Post News
[I] Remove news
your choice is :'''
        option2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        choice = check(menu2, option2)

        # Adding a student
        if choice == 'A':
            while True:
                student_id = input("Enter Student ID: ")

                cr.execute("SELECT id FROM students")
                students_ids = cr.fetchall()

                # Check that the student is not in database
                if (student_id,) not in students_ids:
                    break
                else:
                    print("This student is actually in the system.")
                    print("====================================")

            # Taking Data
            student = input("Enter Student Name: ")
            grade = gpa_grade_check(1, 'Grade')
            gpa = gpa_grade_check(0, 'GPA')
            ps = input("Enter Student password:")

            # inserting it in our database
            cr.execute(
                f"INSERT INTO students(name,id,grade,GPA,password) VALUES ('{student}','{student_id}',{grade},{gpa},'{ps}')")
            db.commit()

            print("==========================================")
            print('Student information is saved successfully!')
            print("==========================================")

        # Remove a student
        elif choice == 'B':
            while True:
                # taking id from user
                print("Note: All student information will be removed")
                student_id_remove = check_get_id()
                print("=============================================")

                cr.execute('SELECT * FROM students WHERE id = ?', (student_id_remove,))
                student = cr.fetchone()

                # To make sure of remove operation
                warnings = f"""Are you sure you want to remove {student[1]}?
[A] Yes, remove the student
[B] No, Do not remove the student
Your answer(A/B): """
                warnings_option = ['A', 'B']
                choice_warning = check(warnings, warnings_option)

                if choice_warning == 'A':
                    # removing it
                    cr.execute(f"DELETE FROM students WHERE id = {student_id_remove}")
                    db.commit()

                    print("====================================")
                    print("==Student is removed successfully!==")
                    print("====================================")

                # Closing the program
                if not continue_or('remove another one'):
                    break

        # Edit student information
        elif choice == 'C':
            # getting id
            id2 = check_get_id()

            # the information that the control can edit(The remain are edited by the student)
            while True:
                # Menu 4
                menu4 = """What do you want to change?
[A] Student GPA
[B] Student Password
[C] Student Grade            
[D] Student Name
[E] Student ID
Your choice: """
                option4 = ['A', 'B', 'C', 'D', 'E']
                choice4 = check(menu4, option4)

                # To modify GPA
                if choice4 == 'A':
                    student_GPA = gpa_grade_check(0, 'GPA')
                    cr.execute(f"UPDATE students SET gpa = {student_GPA} WHERE id = {id2}")

                    print("====================================")
                    print("Student GPA is updated successfully!")
                    print("====================================")

                # To modify the password
                elif choice4 == 'B':
                    student_pass = input("Enter Student password :")
                    cr.execute(f"UPDATE students SET password = '{student_pass}' WHERE id = {id2}")

                    print("=========================================")
                    print("Student Password is updated successfully!")
                    print("=========================================")

                # to modify the grade
                elif choice4 == 'C':
                    # to check the limit of entered grade
                    student_Grade = gpa_grade_check(1, 'Grade')
                    cr.execute(f"UPDATE students SET grade = {student_Grade} WHERE id = {id2}")

                    print("======================================")
                    print("Student Grade is updated successfully!")
                    print("======================================")

                # to modify the name
                elif choice4 == 'D':
                    student_name = input("Enter Student name: ")
                    cr.execute(f"UPDATE students SET name = '{student_name}' WHERE id = {id2}")

                    print("=====================================")
                    print("Student Name is updated successfully!")
                    print("=====================================")

                # to modify the ID
                else:
                    cr.execute("SELECT id from students")
                    student_IDs = cr.fetchall()
                    while True:
                        student_N_id = input("Enter Student new ID: ")
                        if (student_N_id,) in student_IDs or (student_N_id,) == (student_N_id,):
                            print("Please enter another unused ID")
                            print("==============================")
                        else:
                            break

                    cr.execute(f"UPDATE students SET id = '{student_N_id}' WHERE id = {id2}")

                    print("===================================")
                    print("Student ID is updated successfully!")
                    print("===================================")

                db.commit()
                # if he wants to continue editing
                if not continue_or('make another change'):
                    break

                # if he wants to change the id of edit
                if continue_or('change ID'):
                    id2 = check_get_id()

        # To add a course
        elif choice == 'D':
            cr.execute("SELECT * FROM courses")
            courses = cr.fetchall()

            # to check that we cant find the student id
            while True:
                course_name = input("Enter the course name you want to add: ").lower()
                if (course_name,) != courses:
                    break
                else:
                    print("============================")
                    print("This course is already added")

            # adding the course to our database
            cr.execute(f"INSERT INTO courses(course) VALUES ('{course_name}')")
            db.commit()

            print("============================================")
            print(f"{course_name} is added to the courses table")
            print("============================================")

        # to remove a course that is added before
        elif choice == 'E':
            while True:
                cr.execute("SELECT * FROM courses")
                courses = cr.fetchall()

                # To print all the courses added before to choose between them
                for key, (i,) in enumerate(courses):
                    print(f"{key + 1}.{i}")

                # Check of the presence of the course he wants to remove
                while True:
                    print("============================")
                    course_name = input("Enter the course name you want to remove: ").lower()
                    if (course_name,) not in courses:
                        print(f"{course_name} is not found")
                    else:
                        break

                # To make sure of remove operation
                warnings = f"""Are you sure you want to remove {course_name}?
[A] Yes, remove {course_name}
[B] No, Do not remove {course_name}
Your answer(A/B): """
                warnings_option = ['A', 'B']
                choice_warning = check(warnings, warnings_option)

                if choice_warning == 'A':
                    # to delete it
                    cr.execute(f"DELETE FROM courses WHERE course = '{course_name}'")
                    db.commit()

                    print("============================================")
                    print(f"{course_name} is removed from the courses table")
                    print("============================================")

                # Closing the program
                if not continue_or('remove another one'):
                    break

        elif choice == 'F':
            while True:
                student_ID = check_get_id()
                cr.execute(f"select course from course_for_student where id = '{student_ID}'")
                list_of_courses = cr.fetchall()

                cr.execute('SELECT * FROM students WHERE id = ?', (student_ID,))
                student_info = cr.fetchone()
                print("===============================================")
                print(f"Information for Student ID {student_info[0]}:")
                print(
                    f"""-Name of the student: {student_info[1]}
-Grade of the student: {student_info[2]}
-GPA of the student: {student_info[3]}
-Password: {student_info[4]}
-Group Type: {student_info[5]}
-course assigned:""", end=' ')

                if list_of_courses:
                    for row in list_of_courses:
                        print(row[0], end=", ")
                else:
                    print("No courses")
                print("===============================================")

                if not continue_or("retrieve information for another student"):
                    break

        elif choice == 'G':
            cr.execute('SELECT * FROM students')
            students = cr.fetchall()

            cr.execute(f"select course from course_for_student")
            list_of_courses = cr.fetchall()

            print("\n====List of Students===")
            for student in students:
                print(
                    f"""ID: {student[0]} | Name: {student[1]} | Grade: {student[2]} | GPA: {student[3]} |\
Password: {student[4]} | Group Type: {student[5]}| Courses assigned: """, end=' ')
                if list_of_courses:
                    for row in list_of_courses:
                        if row is not row[len(list_of_courses)-1]:
                            print(row[0], end=", ")
                    print(list_of_courses[len(list_of_courses)-1])
                else:
                    print("No courses")
                print("================================================================================================\
=========================================================================================")

        elif choice == 'H':

            while True:
                news_content = input("Enter the news content: ")
                print("======================================")
                if not news_content.strip():
                    print("\nNews content cannot be empty. Please enter some text.")
                    print("======================================")

                    continue

                cr.execute('INSERT INTO news (news) VALUES (?)', (news_content,))
                db.commit()
                print("============================")
                print("==News added successfully!==")
                print("============================")

                choice_of_news = continue_or("add another new article")
                if choice_of_news == 'B':
                    break

        else:
            while True:
                news_diction = {}

                cr.execute("SELECT * FROM news")
                news = cr.fetchall()

                for i in range(1, len(news)):
                    news_diction[str(i)] = news[i-1][0]
                for key, value in news_diction.items():
                    print(key, ':', value)

                num = "which news that you want to remove?"
                option_news = news_diction.keys()
                news_num = check(num, option_news)

                cr.execute(f"DELETE FROM news WHERE news = '{news_diction[news_num]}'")

                print("==================================")
                print("this news is removed successfully!")
                print("==================================")

                if not continue_or("another news"):
                    break

        # Closing the program
        if not continue_or('preform another function'):
            print('==Thanks For using our Program==')
            break

elif choice == 'B':
    cr.execute("select * from courses")
    list_of_coursesA = cr.fetchall()

    # login
    cr.execute("select id, password from students")
    saved_credentials = cr.fetchall()
    print("==== Student sign =====")
    while True:
        student_id = input("Please enter your ID: ").capitalize()
        student_pass = input("Please enter your password: ")
        if (student_id, student_pass) in saved_credentials:
            break
        else:
            print("========================")
            print("Invalid name or password")

    cr.execute(f"select name from students where id = {student_id}")
    student_name = cr.fetchone()

    print("========================")
    print(f"Welcome {student_name[0]}")
    while True:
        student_menu = """[A] Register courses
[B] Edit courses
[C] Choose the group
[D] See news
[E] Exit
Please Choose: """
        option_student = ['A', 'B', 'C', 'D', 'E']
        choices = check(student_menu, option_student)

        if choices == "A":
            register_courses(student_id)

        elif choices == "B":
            edit_courses()
            db.commit()

        elif choices == "C":
            chosen_group()
            db.commit()

        elif choices == "D":
            cr.execute("select * from news")
            news = cr.fetchall()
            for new in news:
                print(new[0])
                print("===============================================================================================")

        elif choices == "E":
            db.close()
            print('==Thanks For using our Program==')
            break

        # Closing the program
        if not continue_or('preform another function'):
            print('==Thanks For using our Program==')
            break

else:
    print('==Thanks For using our Program==')
