from flask import Flask, render_template, request
import job_handler

app = Flask(__name__)

@app.route('/')
def mainpage():
   return render_template("main.html")

@app.route('/api/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == "GET":
        return "Not yet implemented"
    else: 
        json_data = request.get_json()
        job_handler.addJob(json_data)
        return "Added job"
        
