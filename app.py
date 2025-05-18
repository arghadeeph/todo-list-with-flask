from db import conn
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

cursor = conn.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks")
    alltasks = cursor.fetchall() 

    cursor.execute("SELECT * FROM tasks where is_done = %s", ('0', ))   
    activetasks = cursor.fetchall() 

    cursor.execute("SELECT * FROM tasks where is_done = %s", ('1', ))   
    completedtasks = cursor.fetchall() 

    return render_template('index.html', tasks=alltasks, activetasks=activetasks, completedtasks=completedtasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    cursor.execute("INSERT INTO tasks (task) values (%s)", (task,))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    return redirect('/')

@app.route('/checkbox-action/<int:task_id>', methods=['POST'])
def doneNotDone(task_id):
    data = request.get_json()
    is_done = data.get('value')
    new_is_done = 1 - int(is_done)
    cursor.execute("UPDATE tasks set is_done = %s WHERE id = %s", (new_is_done, task_id))
    conn.commit()
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)