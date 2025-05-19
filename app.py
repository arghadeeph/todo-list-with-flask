from db import conn
from flask import Flask, render_template, request, redirect, jsonify, flash
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

cursor = conn.cursor()

# Configuration for mail server (example using Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'arghadeeph@gmail.com'
app.config['MAIL_PASSWORD'] = 'oetlfgpykaignzej'  # Use app password, not Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'arghadeeph@gmail.com'

mail = Mail(app)

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

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        cursor.execute("INSERT INTO contact_us (name, email, subject, message) values (%s, %s, %s, %s)", (name, email, subject, message))
        conn.commit()
        msg = Message(
        subject=subject,
        recipients=[email],  # Change this
        body=message
        )
        mail.send(msg)
        flash('Thank you! Your message has been sent successfully.', 'success')
        return redirect('/contact')
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)