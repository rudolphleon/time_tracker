from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    total_time = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    return render_template('input_form.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    project_name = request.form['project_name']
    topic_name = request.form['topic_name']
    
    # Update total time for the project in the database
    project = Project.query.filter_by(name=project_name).first()
    if project:
        project.total_time += 1
    else:
        new_project = Project(name=project_name, total_time=1)
        db.session.add(new_project)
    db.session.commit()
    
    # Redirect to the timer display route
    return redirect(url_for('timer_display', project=project_name, topic=topic_name))


@app.route('/timer_display')
def timer_display():
    project_name = request.args.get('project')
    topic_name = request.args.get('topic')
    
    # Retrieve total time for the project from the database
    project = Project.query.filter_by(name=project_name).first()
    total_time = project.total_time if project else 0
    
    # Render the timer display template with the project, topic, and total time
    return render_template('timer_display.html', project=project_name, topic=topic_name, total_time=total_time)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
