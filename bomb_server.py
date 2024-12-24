import sys
import subprocess

BOT_COUNT = 10

procs = []
for i in range(BOT_COUNT):
    proc = subprocess.Popen([sys.executable, 'bomb.py', '{}in.csv'.format(i), '{}out.csv'.format(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()