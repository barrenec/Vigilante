
from flask import Flask, request, render_template, flash, redirect, session, url_for, Markup
import os.path
from models import Schedule
from models import Request
from forms import ScheduleForm
from flask_peewee.utils import PaginatedQuery


# app config
app = Flask(__name__)
app.debug = True
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.secret_key = 'super secret key'


@app.route('/')
def index():
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
        handle_form_errors(form.errors)

    return render_template("form.html", form=form)


@app.route('/edit/<int:id>/', methods={'POST', 'GET'})
def edit(id):
    form = ScheduleForm(obj=Schedule.select().where(Schedule.id == id).get())
    if form.validate_on_submit():

        if 'active' in request.form:
            active = 1
        else:
            active = 0

        Schedule.update(name=request.form['name']
                        , url=request.form['url']
                        , check_interval=request.form['check_interval']
                        , active=active
                        ).where(Schedule.id == id).execute()
        flash('Your actor has been updated', 'success')
        return redirect(url_for('index'))
    elif form.errors:
        handle_form_errors(form.errors)

    return render_template("form.html", form=form)


@app.route('/delete/<int:id>/', methods={'POST'})
def delete(id):
    Schedule.delete().where(Schedule.id == id).execute()
    flash('Your actor has been deleted', 'warning')
    return redirect(url_for('index'))


@app.route('/details/<int:id>/')
@app.route('/details/<int:id>/page/<int:page>')
def details(id, page=20):
    actor = Schedule.select().where(Schedule.id == id).get()
    actor_requests = Request.select().where(Request.url_id == id).order_by(Request.insert_date.desc())
    pages = PaginatedQuery(actor_requests, page)
    content = pages.get_list()

    stats = {}
    stats['site_changes'] = actor_requests.select(Request.content_len).distinct().count()
    stats['total_hits'] = actor_requests.count()
    stats['ok_hits'] = actor_requests.select(Request.id).where(Request.status_code == '200').count()
    stats['avg_response_time'] = (sum([row.response_time for row in actor_requests])/stats['total_hits'])

    return render_template('details.html', actor=actor, actor_requests=content, pages=pages, stats=stats)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# only functions no actions
def handle_form_errors(errors):
    error_string = ""
    for fieldName, errorMessages in errors.iteritems():
        for err in errorMessages:
            error_string +=  fieldName + ': ' + err + '<br>'
    flash(Markup(error_string), 'danger')


# view helpers/ template filters
@app.template_filter('format_date')
def format_date(date):
    return date.strftime("%d.%m.%y %X")


@app.template_filter('format_response_time')
def format_response_time(time):
    return time.strftime("%S.%f")[:6]


if __name__ == "__main__":
    app.run()
