import sqlite3


class Stats:
   conn = sqlite3.connect(':memory:', check_same_thread=False)

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
      conn = self.conn
      c = conn.cursor()
      c.execute("DELETE from stats WHERE jobName = '" + jobname + "'")
      self.conn.commit()
