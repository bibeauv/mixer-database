import subprocess
import os

cmd = "sq -u bibeauv -h -t pending,running -r | wc -l"
running_jobs = int(os.popen(cmd).read())
print(running_jobs)
