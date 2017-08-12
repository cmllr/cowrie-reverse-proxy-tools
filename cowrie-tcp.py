import subprocess
import datetime
import time
from subprocess import check_output

verbose = True
port = 22223
log = {}

class State:
  def __init__(self):
    self.date = None;
    self.state = ""
  def __repr__(self):
    return '{} ({})'.format(self.state,self.date)

def getInfos(line):
  parts = line.split(b";");
  portStart = parts[0].rfind(b":")
  ip = parts[0][:portStart]
  state = parts[1]
  s = State();
  s.date = datetime.datetime.now()
  s.state = state
  if ip not in log:
    log[ip] = [s]
    if verbose:
      output("{} new state {} ({})".format(s.date, ip,s.state));
  else:
    stateExisting = False
    for existingState in log[ip]:
      if (existingState.state == s.state):
        stateExisting = True
        if (existingState.state != s.state):
          output("{} state change {} => {} ({})".format(s.date,ip,existingState.state, s.state));
        break;
    if (s not in log[ip] and stateExisting == False):
      output("{} state change {} ({})".format(s.date, ip,s.state));

def run():
  command = "netstat -tn 2>/dev/null | grep :"+ port + "  | awk '{print $5 \";\" $6}'"
  output = check_output(command, shell=True)
  outputLines = output.split(b"\n");
  for line in outputLines:
    if line:
      getInfos(line)

def output(what):
  with open("./tcp.log", "ab") as myfile:
    myfile.write(bytes(what+"\n",'UTF-8'))
  print(what)

while True:
  run();

