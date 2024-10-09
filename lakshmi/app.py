from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import StudentTracker  # Import the StudentTracker class

app = Flask(__name__)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('student.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS student_details (
                roll_number TEXT PRIMARY KEY,
                name TEXT,
                class TEXT,
                section TEXT              
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS marks_details (
                roll_number TEXT,
                subject TEXT,
                grade TEXT,
                marks INT              
            
                              )
            """)
        print("Database table created successfully.")

    def add_student(self, roll_number, name,classs,section):
        with self.conn:
            self.conn.execute("INSERT INTO student_details (roll_number, name,class,section) VALUES (?, ?,?,?)", (roll_number, name,classs,section))
    def add_grade(self, roll_number,subject,grade,marks):
        with self.conn:
            self.conn.execute("INSERT INTO marks_details(roLL_number,subject,grade,marks) VALUES (?,?,?,?)", (roll_number,subject,grade,marks))        

    def get_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM student_details")
        return cursor.fetchall()
    def get_all_grades(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM marks_details")
        return cursor.fetchall()
    def delete(self, roll_number):
      with self.conn:
        self.conn.execute("DELETE FROM marks_details WHERE roll_number=?", (roll_number,))
        self.conn.execute("DELETE FROM student_details WHERE roll_number=?", (roll_number,))

    def cal_average(self, roll_number):
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG(marks) FROM marks_details WHERE roll_number=?", (roll_number,))
        average = cursor.fetchone()[0]  
        return average if average is not None else 0  


            

# Instantiate the Database and StudentTracker classes
database = Database()
tracker = StudentTracker()

@app.route('/')
def start():
   return  render_template('home.html')
@app.route('/form')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    roll_number = request.form['roll_number']
    name = request.form['name']
    classs=request.form['classs']
    section=request.form['section']
    database.add_student(roll_number, name,classs,section)
    tracker.add_student(name, roll_number,classs,section)  # Add student to the tracker
    return redirect(url_for('index'))
@app.route('/form2')
def grade():
    return render_template('grades.html')
@app.route('/add_grades' ,methods=['POST'])
def add_grades():
    roll_number=request.form['roll_number']
    subject=request.form['subject']
    grade=request.form['grade']
    marks=request.form['marks']
    database.add_grade(roll_number,subject,grade,marks)
    #tracker.cal_average(roll_number,marks)
    tracker.add_grades(roll_number,subject,grade)
    return redirect(url_for('index'))
@app.route('/students')
def view_students():
    students = database.get_all_students()  # Fetch all students from the database
    grades=database.get_all_grades()
    return render_template('student_details.html', student_details=students,marks_details=grades)
@app.route('/delete_form')
def form():
    return render_template('delete.html')
@app.route('/delete',methods=['POST'])
def delete():
    roll_number=request.form['roll_number']
    database.delete(roll_number)
    return render_template('message.html')
@app.route('/average_form')
def average():
    return render_template('average.html')
@app.route('/average', methods=['POST'])
def cal_average():
    roll_number = request.form['roll_number']
    average = database.cal_average(roll_number)
    print(f'Calculated average for {roll_number}: {average}')  # Debug print
    return render_template('message1.html', roll_number=roll_number, average=average)

    


if __name__ == "__main__":
    app.run(debug=True)

    