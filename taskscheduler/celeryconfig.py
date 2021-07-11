from datetime import timedelta

config = {
    "broker_url":"pyamqp://guest@localhost//",
    "task_serializer":"json",
    "result_serializer":'json',
    "accept_content":['json'],
    # "timezone":'Europe/Dublin',
    "enable_utc":True,
    "beat_schedule":{
    "call-DB-at-12": {
        'task': 'get-tasks',
        'schedule': timedelta(seconds=5)
    },
    'every-10-sec':{
        'task':'display',
        'schedule':timedelta(seconds=10)
    }
}

}