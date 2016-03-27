
from flask import Flask, request, render_template, flash, redirect, session, url_for
import os.path
from models import Request
from models import Schedule

app = Flask(__name__)
app.debug = True
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.secret_key = 'super secret key'


@app.route('/')
def index():
    #query = (Request.select(Request, Schedule).join(Schedule).limit(10)).sql()
    #data = Request.raw(query[0])
    data = Schedule.select()
    return render_template("index.html", data=data)


@app.route('/create', methods={'POST', 'GET'})
def create():
    form_data = {"name": "", "url": "", "check_interval": ""}
    if request.method == 'POST':
        form_data = request.form
        Schedule.create(name=form_data['name']
                        , url= form_data['url']
                        , check_interval=form_data['check_interval'])
        flash('Your actor has been created', 'success')
        return redirect(url_for('index'))
    return render_template("form.html", data=form_data)


@app.route('/edit/<int:id>/', methods={'POST', 'GET'})
def edit(id):
    form_data = Schedule.select().where(Schedule.id == id).get()
    if request.method == 'POST':
        Schedule.update(name=request.form['name']
                        , url=request.form['url']
                        , check_interval=request.form['check_interval']
                        ).where(Schedule.id == id).execute()
        flash('Your actor has been updated', 'success')
        return redirect(url_for('index'))
    return render_template("form.html", data=form_data)


@app.route('/delete/<int:id>/', methods={'POST'})
def delete(id):
    Schedule.delete().where(Schedule.id == id).execute()
    flash('Your actor has been deleted', 'warning')
    return redirect(url_for('index'))


def validate_form(form_data):
    pass


if __name__ == "__main__":
    app.run()
