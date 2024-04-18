from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# This dictionary will store the timers for each project and topic
timers = {}

@app.route('/')
def index():
    return render_template('input_form.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    project_name = request.form['project_name']
    topic_name = request.form['topic_name']
    
    # Start the timer for the project and topic
    timers[(project_name, topic_name)] = time.time()
    
    # Redirect to the timer display route
    return redirect(url_for('timer_display', project=project_name, topic=topic_name))

@app.route('/timer_display')
def timer_display():
    project_name = request.args.get('project')
    topic_name = request.args.get('topic')
    start_time = timers.get((project_name, topic_name), None)
    if start_time is None:
        return "Timer not started for the specified project and topic."
    
    elapsed_time = time.time() - start_time
    
    # Render the timer display template with the project, topic, and elapsed time
    return render_template('timer_display.html', project=project_name, topic=topic_name, elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run(debug=True)
