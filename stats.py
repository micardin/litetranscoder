import sqlite3


class Stats:
   conn = sqlite3.connect(':memory:', check_same_thread=False)

   def initStats(self):
       c = self.conn.cursor()
       c.execute('''CREATE TABLE stats 
           (jobname text PRIMARY KEY, fps text, bitrate text, total_size text, out_time text, dup_frames text, drop_frames text, speed text, progress text)''')
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
       c.execute("REPLACE INTO stats(jobname, fps, bitrate, total_size, out_time, dup_frames, drop_frames, speed, progress) VALUES ('" + jobname + "','" + jobdict['fps'] + "','" + jobdict['bitrate'] + "','" + jobdict['total_size'] + "','" + jobdict['out_time'] + "','" + jobdict['dup_frames'] + "','" + jobdict['drop_frames'] + "','" + jobdict['speed'] + "','" + jobdict['progress'] + "')")
       self.conn.commit()
       
   def getStats(self, jobname):
      conn = self.conn
      conn.row_factory = self.sqltoJson
      c = conn.cursor()
      c.execute("SELECT * FROM stats WHERE jobname=?", (jobname,))
      result = c.fetchone()
      print(result)
      return result
