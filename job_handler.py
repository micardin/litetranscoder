from ffmpy import FFmpeg
from multiprocessing import Process

def jobThread(ff):
    ff.run()

def addJob(json):
    ffjob = FFmpeg(
        inputs={json['input']: None},
        outputs={json['output']: None}
    )
    p = Process(target=jobThread, args=(ffjob,))
    p.start()
    print("Job added:", json)
