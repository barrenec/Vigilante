
from flask import Flask, request, render_template, flash, redirect, session, url_for, Markup
import os.path
from models import Request
from models import Schedule
from forms import ScheduleForm

# app config
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
    form = ScheduleForm()
    if form.validate_on_submit():
        Schedule.create(name=form['name'].data
                        , url= form['url'].data
                        , check_interval=form['check_interval'].data)
        flash('Your actor has been created', 'success')
        return redirect(url_for('index'))
    elif form.errors:
        error_string = ""
        for fieldName, errorMessages in form.errors.iteritems():
            for err in errorMessages:
                error_string +=  fieldName + ': ' + err + '<br>'
        flash(Markup(error_string), 'danger')

    return render_template("form.html", form=form)


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


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
