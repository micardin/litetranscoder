from ffmpy import FFmpeg, FFRuntimeError
from multiprocessing import Process
from threading import Thread

jobs=[]

def outputBuilder(json):
    outputopts = ""
    
    if 'framerate' in json:
       outputopts += " -r " + json['framerate']
    if 'vcodec' in json:
       outputopts += " -c:v " + json['vcodec']
    if 'vbitrate' in json:
       outputopts += " -b:v " + json['vbitrate']
    if 'resolution' in json:
       outputopts += " -s " + json['resolution']
       
    return outputopts
    
def inputBuilder(json):
    inputopts = ""
    
    if 'input_loop' in json:
       inputopts += "-stream_loop -1 "
    if 'realtime' in json:
       inputopts += "-re "
    
    if inputopts == "":
       return None
    else:
       return inputopts

def jobThread(ff):
    try:
       ff.run()
    except FFRuntimeError as ex:
       pass

def addJob(json):
    globalopts = "-y -hide_banner -progress http://localhost:5000/api/stats/"+ json['name'],
    inputopts = inputBuilder(json)
    outputopts = outputBuilder(json)
    
    ffjob = FFmpeg(
        global_options=globalopts,
        inputs={json['input']: inputopts},
        outputs={json['output']: outputopts}
    )
    process = Thread(target=jobThread, args=(ffjob,))
    process.start()
    jobs.append([json['name'], ffjob])
    print("Job added:", json)
    
def stopJob(json):
   for job in jobs:
       if job[0] == json['name']:
           job[1].process.terminate()
