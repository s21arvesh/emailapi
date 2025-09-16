"""
import schedule

import time as tm
from datetime import time, timedelta, datetime


def job():
    print(" THIS IS JUST FOR TEST PURPOSE ")


schedule.every(2).seconds.do(job)

while True:
    schedule.run_pending()
    tm.sleep(1)
"""

with open('/Users/sarvesh_21/Documents/project_file/py-flask-structure/smth.txt', 'r') as f:
    for i in f:
        if 'CTRL+C' in i:
            print(i[0:23])
