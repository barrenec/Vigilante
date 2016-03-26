from models import Request
from models import Schedule


id = 1
form_data = Schedule.select().where(Schedule.id == id).get()

print form_data.name

exit()

query = (Request.select(Request, Schedule).join(Schedule, 'LEFT OUTER').limit(10)).sql()
print query

data = Request.raw(query[0])

for row in data:
    print row.name

