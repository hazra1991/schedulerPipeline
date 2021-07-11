from tools import CeleryTask

celery_app = CeleryTask('Task-Scheduler')


##### define tasks below #######


@celery_app.add_task_proxy
# @celery_app.block_exe
def proxy_task1():
    from testfunfile import fun1
    fun1()


# @celery_app.add_logs
@celery_app.add_task_proxy
def proxy_task2(a,b,c,d):

    print(a,b,c,d)
    # from testfunfile import fun2
    # fun2()



