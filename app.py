from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

bus_location = "School"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_students=total_students
    )


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        stop_name = request.form['stop_name']
        parent_phone = request.form['parent_phone']

        conn = sqlite3.connect('schoolbus.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, stop_name, parent_phone) VALUES (?, ?, ?)",
            (name, stop_name, parent_phone)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_student.html')


@app.route('/view_students')
def view_students():

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template('view_students.html', students=students)


@app.route('/search_student', methods=['GET', 'POST'])
def search_student():

    students = []

    if request.method == 'POST':

        name = request.form['name']

        conn = sqlite3.connect('schoolbus.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + name + '%',)
        )

        students = cursor.fetchall()

        conn.close()

    return render_template('search_student.html', students=students)


@app.route('/delete_student/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view_students')


@app.route('/add_route', methods=['GET', 'POST'])
def add_route():

    if request.method == 'POST':

        route_name = request.form['route_name']
        start_location = request.form['start_location']
        end_location = request.form['end_location']

        conn = sqlite3.connect('schoolbus.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO routes (route_name, start_location, end_location) VALUES (?, ?, ?)",
            (route_name, start_location, end_location)
        )

        conn.commit()
        conn.close()

        return redirect('/view_routes')

    return render_template('add_route.html')


@app.route('/view_routes')
def view_routes():

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()

    conn.close()

    return render_template('view_routes.html', routes=routes)


@app.route('/notifications', methods=['GET', 'POST'])
def notifications():

    if request.method == 'POST':

        message = request.form['message']

        conn = sqlite3.connect('schoolbus.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO notifications (message) VALUES (?)",
            (message,)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()

    conn.close()

    return render_template(
        'notifications.html',
        notifications=notifications
    )


@app.route('/delete_notification/<int:id>')
def delete_notification(id):

    conn = sqlite3.connect('schoolbus.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notifications WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/notifications')


@app.route('/bus_tracking', methods=['GET', 'POST'])
def bus_tracking():

    global bus_location

    if request.method == 'POST':
        bus_location = request.form['location']

    return render_template(
        'bus_tracking.html',
        current_location=bus_location
    )


if __name__ == '__main__':
    app.run(debug=True)