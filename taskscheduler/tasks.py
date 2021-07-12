from tools import CeleryTask

#########################################
# celelry application : dont change or delete

celery_app = CeleryTask('Task-Scheduler')

#########################################

##### define proxy tasks for you tasks below #######


@celery_app.add_task(plug_to='schedule-tasks-from-DB')
# @celery_app.block_exc
def proxy_task1(*arg,**kw):
    # from testfunfile import fun1
    # fun1()
    print(arg,kw)


# @celery_app.add_logs
@celery_app.add_task(plug_to="schedule-tasks-from-DB")
def proxy_dummytask(*arg , **kw):
    print(arg,kw)