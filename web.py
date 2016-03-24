
from flask import Flask, request, render_template
import os.path
from models import Request
from models import Schedule

app = Flask(__name__)
app.debug = True
app.root_path = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    query = (Request.select(Request, Schedule).join(Schedule).limit(10)).sql()
    data = Request.raw(query[0])

    return render_template("index.html", data=data)


if __name__ == "__main__":
   app.run()
