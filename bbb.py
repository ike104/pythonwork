from dateutil.parser import parse
import time

d = 'Jun 1 15:50pm'
print d
y=parse(d).strftime("%Y-%m-%d %H:%M")
print y

d = 'Jun 1 aa'
print d
try:
    y=parse(d).strftime("%Y-%m-%d %H:%M")
except ValueError:
    y=''
print y

d = 'Jun 30 13:00pm'
print d
try:
    y=parse(d).strftime("%Y-%m-%d %H:%M")
except ValueError:
    y=''
print y
