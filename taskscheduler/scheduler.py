from datetime import timedelta,datetime
from tasks import celery_app
from celeryconfig import config

### update config ###
celery_app.conf.update(config)


time = datetime.utcnow() + timedelta(seconds=30)


##### define heart beet tasks ########
@celery_app.task(name='get-tasks')
def get_():
    print('it is returned')

@celery_app.task(name='display')
def display():
    print('display')


# # testfunfile.fun1.apply_async(args=(12,),eta =datetime.utcnow() + timedelta(seconds=30))
# import time as t

# # t.sleep(10)
# for i in range(3):
#     # fun1.apply_async(args=(12,),eta=time)
#     print('dasdasd')
#     pass