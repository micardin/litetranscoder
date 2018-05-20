import sqlite3
import time


class Stats:
   conn = sqlite3.connect(':memory:', check_same_thread=False)
   statlock = {}

   #create in-memory sqlite3 table for stats tracking
   def initStats(self):
       c = self.conn.cursor()
       c.execute('''CREATE TABLE stats 
           (jobName text PRIMARY KEY, fps text, bitrate text, totalSize text, uptime text, dupFrames text, dropFrames text, speed text, status text)''')
       self.conn.commit()
       
   def sqltoJson(self, cursor, row):
       d = {}
       for idx, col in enumerate(cursor.description):
           d[col[0]] = row[idx]
       return d

   #insert stats
   def ingestStats(self, jobname, chunk):
       jobdict = {}
       splitchunk = chunk.decode("utf-8").split('\n')
       for item in splitchunk:
           isplit = item.split('=')
           if len(isplit) == 2:
               jobdict[isplit[0]] = isplit[1]
       c = self.conn.cursor()
       status = "Unknown"
       if jobdict['progress'] == "continue":
           status = "Running"
       else:
           status = "Stopped"
       #if job has been removed within 5 seconds, don't re-add it to the table
       if jobname in self.statlock:
           if self.statlock[jobname] <= time.time() + 5:
               return
           else:
               del self.statlock[jobname]
       c.execute("REPLACE INTO stats(jobName, fps, bitrate, totalSize, uptime, dupFrames, dropFrames, speed, status) VALUES ('" + jobname + "','" + jobdict['fps'] + "','" + jobdict['bitrate'] + "','" + jobdict['total_size'] + "','" + jobdict['out_time'].split('.')[0] + "','" + jobdict['dup_frames'] + "','" + jobdict['drop_frames'] + "','" + jobdict['speed'] + "','" + status + "')")
       self.conn.commit()
       
   def getStats(self, jobname):
      conn = self.conn
      conn.row_factory = self.sqltoJson
      c = conn.cursor()
      c.execute("SELECT * FROM stats WHERE jobname=?", (jobname,))
      result = c.fetchone()
      return result
  
   def getAllStats(self):
      statsobj = {}
      conn = self.conn
      conn.row_factory = self.sqltoJson
      c = conn.cursor()
      c.execute("SELECT * FROM stats")
      result = c.fetchall()
      statsobj["data"] = result
      return statsobj
  
   def removeJob(self, jobname):
      self.statlock[jobname] = time.time()
      conn = self.conn
      c = conn.cursor()
      c.execute("DELETE from stats WHERE jobName = '" + jobname + "'")
      self.conn.commit()
      
