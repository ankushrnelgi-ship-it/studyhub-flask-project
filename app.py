from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():

    if request.method == 'POST':

        task = request.form['task']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks(task, status) VALUES(?, ?)",
            (task, 'Pending')
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_task.html')


@app.route('/complete/<int:id>')
def complete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/stats')
def stats():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
    )

    completed = cursor.fetchone()[0]

    pending = total - completed

    conn.close()

    return render_template(
        'stats.html',
        total=total,
        completed=completed,
        pending=pending
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)