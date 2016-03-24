from peewee import *
from datetime import datetime


class Models:

    database = SqliteDatabase('Vigilante.db')

    def config(self):

        schedule_model = Schedule()
        if not schedule_model.table_exists():
            schedule_model.create_table()

        request_model = Request()
        if not request_model.table_exists():
            request_model.create_table()

    def create_defaults(self):

        schedule_object = Schedule()

        if schedule_object.select().count() == 0:

            # myTT
            schedule_object = Schedule(
                name="Mytt Public Home", url="http://www.mytischtennis.de/public/home")
            schedule_object.save()

            # golf.de
            schedule_object = Schedule(
                name="Golf.de Home", url="http://www.golf.de/publish/home")
            schedule_object.save()


class BaseModel(Model):

    class Meta:
        database = Models().database


class Schedule(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = CharField()
    url = CharField()
    check_interval = IntegerField(default=1 * 60)
    check_interval_unit = CharField(default='s')
    check_from = DateTimeField(null=True)
    check_to = DateTimeField(null=True)


class Request(BaseModel):
    id = PrimaryKeyField(unique=True)
    url_id = ForeignKeyField(rel_model=Schedule)
    status_code = CharField()
    response_time = TimeField()
    insert_date = DateTimeField(default=datetime.now())
    server = CharField(null=True)
    content_len = IntegerField(null=True)


model_object = Models()
model_object.config()
model_object.create_defaults()
