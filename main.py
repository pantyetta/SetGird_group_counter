import datetime
import sqlite3
import sys
import time
import subprocess

args = sys.argv

if len(args) < 4:
    print('need group_id & sql path.')
    sys.exit()

sqlPath = args[1]
group_id = int(args[2])
max = int(args[3])

conn = sqlite3.connect(sqlPath)

unUpdateCunt = 0
buffer = 0

try:
    c = conn.cursor()
    while True:
        c.execute('select * from point where group_id = ?', (group_id,))
        result = c.fetchall()
        
        dt_now = datetime.datetime.now()
        size = len(result)
        sys.stdout.write("\r{} | group_id: {}, {}".format(dt_now.strftime('%Y-%m-%d %H:%M:%S'), group_id, size))
        sys.stdout.flush()
        
        if(buffer == size):
            unUpdateCunt += 1
        else:
            buffer = size
            unUpdateCunt = 0
            
        if(unUpdateCunt > 10):
            notice = ['osascript', '-e', f'display notification "Group {group_id} is not update." sound name "Sosumi"']
            subprocess.run(notice)
            unUpdateCunt = 0
        
        
        if(max-7 < size and size < max-5):
            notice = ['osascript', '-e', f'display notification "Group {group_id}" sound name "Hero"']
            subprocess.run(notice)
        time.sleep(2)
        
except KeyboardInterrupt:
    print('\nexit')
finally:
    conn.close()
