from peewee import *
# import

db = PostgresqlDatabase('patient', user='postgres', password='test123',host='127.0.0.1', port=5432)
# # db = PostgresqlDatabase('new')

# class BaseModel(Model):
#     class Meta:
#         database = db  # connection with database

# # Patient model
# class Patient(BaseModel):
#     id = AutoField(column_name='ID')
#     phone = TextField(column_name='phone', null=True)
#     username = TextField(column_name='username', null=True)
#     gender = TextField(column_name='gender', null=True)
#     timezone = TextField(column_name='timezone', null=True)
#     callstart = TimeField(column_name='callstart', null=True)
#     callend = TimeField(column_name='callend', null=True)
#     type = TextField(column_name='type', null=True)
#     created = DateTimeField(column_name='created', null=True)
#     updated = DateTimeField(column_name='updated', null=True)

#     class Meta:
#         table_name = 'patient'

# # Reminder
# class Reminder(BaseModel):
#     id = AutoField(column_name='ID')
#     text = TextField(column_name='text', null=True)

#     class Meta:
#         table_name = 'reminder'

# # Smart Reminder
# class SmartReminder(BaseModel):
#     id = AutoField(column_name='ID')
#     patient_id = IntegerField(column_name='patientid')
#     reminder_id = IntegerField(column_name='reminderid')

#     easiness = FloatField(column_name='easiness', null=True)
#     interval = IntegerField(column_name='interval', null=True)
#     repetitions = IntegerField(column_name='repetitions', null=True)

#     last_time = DateTimeField(column_name='lasttime', null=True)
#     next_time = DateTimeField(column_name='nexttime', null=True)

#     class Meta:
#         table_name = 'smartreminder'



# print(db)

# from twilio.twiml.voice_response import VoiceResponse, Dial, Gather, Say, Client
# from twilio.rest import Client as Client
# to = "101@49.37.170.172:60562"
# main_number = "+14159186834"

# def call_to_check_bld():
#     """ Function for checking blood pressure and saving results to google spreadsheet """
#     account_sid = "AC52d321df2eb36f8cc4091e57e59f15b3"
#     auth_token = "6a35b8bc2453e5ccb03271f025c61ed7"
#     client = Client(account_sid, auth_token)
#     # call studio flow from Python app

#     execution = client.studio \
#         .flows('FW67aa096da884aaa25108b99149434f9d') \
#         .executions \
#         .create(to='+917023491989', from_=main_number)

# call_to_check_bld()

# db.cursor().execute("INSERT INTO Patient(Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('13333333333', 'Alex', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
# db.cursor().execute("INSERT INTO Patient (Phone, Username, Gender, Timezone, CallStart,CallEnd, Type, Created, Updated) VALUES ('12222222222', 'Lina', 'Male', 'Pacific Standard Time', '16:00:00', '18:00:00', 'Volunteer', now(), now())")
# db.cursor().execute("INSERT INTO Reminder (Text) VALUES ('Get at least 150 minutes per week of moderate-intensity aerobic activity or 75 minutes per week of vigorous aerobic activity, or a combination of both, preferably spread throughout the week.')")
# db.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Add moderate- to high-intensity muscle-strengthening activity (such as resistance or weights) on at least 2 days per week.')")
# db.cursor().execute("INSERT INTO Reminder (Text) VALUES ( 'Spend less time sitting. Even light-intensity activity can offset some of the risks of being sedentary.')")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '1', now())")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '2', now())")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('1', '3', now())")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '1', now())")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '2', now())")
# db.cursor().execute("INSERT INTO SmartReminder (PatientID, ReminderID, NextTime) VALUES ('2', '3', now())")
# db.commit()

# cur = db.execute_sql("select * from patient")
# val = cur.fetchall()
# print(val[0])


