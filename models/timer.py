from flask import Flask, render_template, request, redirect, url_for
from models.timer import Timer

app = Flask(__name__)
timer = Timer()  # Initialize Timer object

@app.route('/')
def index():
    return render_template('input_form.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    project_name = request.form['project_name']
    topic_name = request.form['topic_name']
    timer.start_timer(project_name, topic_name)
    return redirect(url_for('index'))

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    project_name = request.form['project_name']
    topic_name = request.form['topic_name']
    elapsed_time = timer.stop_timer(project_name, topic_name)
    return render_template('timer_display.html', project=project_name, topic=topic_name, elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run(debug=True)
