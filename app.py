from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import time

app = Flask(__name__)
db_path = '/home/leon/workspace/github.com/rudolphleon/time_tracker/timetracker.db'

@app.route('/')
def index():
    return render_template('input_form.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    project_name = request.form['project_name'].strip()
    topic_name = request.form['topic_name']

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if project already exists in the database
        cursor.execute("SELECT * FROM project WHERE name=?", (project_name,))
        project = cursor.fetchone()

        if project:
            # If project exists, update the total time
            cursor.execute("UPDATE project SET total_time = total_time + ? WHERE name=?", (1, project_name))
        else:
            # If project does not exist, insert a new row
            cursor.execute("INSERT INTO project (name, total_time) VALUES (?, ?)", (project_name, 1))

        conn.commit()

    return redirect(url_for('timer_display', project=project_name, topic=topic_name))

@app.route('/timer_display')
def timer_display():
    project_name = request.args.get('project')
    topic_name = request.args.get('topic')

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total_time FROM project WHERE name=?", (project_name,))
        total_time = cursor.fetchone()[0]

    return render_template('timer_display.html', project=project_name, topic=topic_name, total_time=total_time)

if __name__ == '__main__':
    app.run(debug=True)
