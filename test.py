from models import Request
from models import Schedule
import time


id = 2
requests = Request.select().where(Request.url_id == id).order_by(Request.response_time.desc())

for row in requests:
    ms = (int(row.response_time.strftime('%S')) * 1000) + (int(row.response_time.strftime('%f'))/1000)
    Request.update(response_time=ms).where(Request.id == row.id).execute()

print "done"
exit()

query = (Request.select(Request, Schedule).join(Schedule, 'LEFT OUTER').limit(10)).sql()
print query

data = Request.raw(query[0])

for row in data:
    print row.name

 #query = (Request.select(Request, Schedule).join(Schedule).limit(10)).sql()
    #data = Request.raw(query[0])