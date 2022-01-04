#!/usr/bin/python3

# Script: processJobs.py

# Author: Jostein Magnussen-Vik
# Created: 28.10.2021
# Modified: 24.11.2021
# Purpose: Start jobs described in a database.
#
# Database definition:
# CREATE TABLE "jobs" (
#       "jobid" INTEGER UNIQUE,
#       "status"        INT DEFAULT 0,
#       "script"        TEXT,
#       "command"        TEXT,
#       "arguments"     TEST,
#       "inputpath"     TEXT,
#       "outputpath"    TEXT,
#       "start" DATETIME,
#       "end"   DATETIME,
#       PRIMARY KEY("jobid" AUTOINCREMENT));
#
# Status 0: not started
# Status 1: running
# Status 2: finished
# Status 3: failed
#
# crontab example:
#*/15 * * * * python3 processJobs.py processingjobs.db

import sys
import sqlite3
import shutil
import subprocess
import re
import tempfile

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Missing argument: database")
    exit()
  # Fix for databases stored on network mounts:
  tmpDir = tempfile.TemporaryDirectory()
  tmpDB = tmpDir.name + '/tempJobDB.db'
  database = sys.argv[1]
  shutil.copyfile(database, tmpDB)
  conn = sqlite3.connect(tmpDB)

  query = 'SELECT jobid, command, arguments, inputpath, outputpath FROM jobs WHERE status = 0;'
  cursor = conn.execute(query)
  job = cursor.fetchone()
  #for row in cursor:
  if job:
    query = 'UPDATE jobs SET status = 1, start=datetime("now") WHERE jobid = ' + str(job[0]) + ';'  
    cursor = conn.execute(query)
    conn.commit()
    conn.close()

    try:
      shutil.copyfile(tmpDB, database)

      args = [job[1], job[2], job[3], job[4]]
      process = subprocess.Popen(args,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()
      stdout = stdout.decode()
      with open(job[4]+'processJobLog_'+str(job[0])+'.log', mode='w') as processJobLog:
        processJobLog.write(" ".join(args))
        processJobLog.write("\r\n")
        processJobLog.write("\r\nReturncode: " + str(process.returncode))
        processJobLog.write("\r\nOutput:\r\n")
        processJobLog.write(stdout)
        processJobLog.write("\r\nError:\r\n")
        processJobLog.write(stderr.decode())
      print("Output from process:")
      print(stdout)
      print(stderr)
      print("Returncode: " + str(process.returncode))
      status = '2'
      reportPathQuery = ''
      if process.returncode > 0:
        status = '3'
      else:
        regSearch = re.search('Forensic report: (.*)\n', stdout)
        if regSearch:
          reportPathQuery = ', outputpath="' + regSearch.group(1) + '"'

      shutil.copyfile(database, tmpDB)
      conn = sqlite3.connect(tmpDB)
      query = 'UPDATE jobs SET status = ' + status + ', end=datetime("now")' + reportPathQuery + ' WHERE jobid = ' + str(job[0]) + ';'

      cursor = conn.execute(query)
      conn.commit()
      conn.close()
      shutil.copyfile(tmpDB, database)
    except:
      shutil.copyfile(database, tmpDB)
      conn = sqlite3.connect(tmpDB)
      query = 'UPDATE jobs SET status = 3 WHERE jobid = ' + str(job[0]) + ';'
      cursor = conn.execute(query)
      conn.commit()
      conn.close()
      shutil.copyfile(tmpDB, database)
  else:
    conn.close()
  tmpDir.cleanup()
