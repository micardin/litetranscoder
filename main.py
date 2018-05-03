import flask
from flask import Flask, render_template, request, jsonify
import job_handler
from stats import Stats

app = Flask(__name__)
stat = Stats()
stat.initStats()

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
    
@app.route('/api/stopjob', methods=['POST'])
def stopJob():
    json_data = request.get_json()
    job_handler.stopJob(json_data)
    return "Stopped job"

@app.route('/api/stats/<jobname>', methods=['GET', 'POST'])
def stats(jobname):
    if request.method == "GET":
        return jsonify(stat.getStats(jobname))
    else:
        chunk_size = 2048
        while True:
            chunk = flask.request.stream.read(chunk_size)
            if len(chunk) == 0:
                return ""
            stat.ingestStats(jobname, chunk)
    return ""
        
