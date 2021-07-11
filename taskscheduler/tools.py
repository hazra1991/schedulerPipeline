from celery import Celery
from functools import wraps 
from celery.local import PromiseProxy
from celery.app.registry import TaskRegistry


class CeleryTask(Celery):
    def __init__(self,*args,**kw):
        self.unplug_registry = {}
        super().__init__(*args,**kw)

    def add_logs(self,fun):
        print(fun)
        @wraps(fun)
        def inner(*a,**kw):
            va = fun(*a,**kw)
        return inner
    
    def block_exe(self,fun):
        if isinstance(fun,PromiseProxy):
            msg = '[X] cannot block a registered task,use decorator before registering'
            raise RuntimeError(msg)

        self.unplug_registry[fun.__name__] = fun
        def inner(*a,**kw):
            return None
        return fun

    def add_task_proxy(self,*args,**kw):
        fun = args[0]
        if fun.__name__ in self.unplug_registry:
            return
        if not fun.__name__.startswith('proxy_'):
            msg = '[X] use the prefix "proxy_" before the function definition ,or use the "@task" decorator'
            raise RuntimeError(msg)
        # print(type(fun))
        # print(args,kw)
        @self.task
        @wraps(fun)
        def inner(*a,**kw):
            print("adaasdada",a,kw)
            fun(*a,**kw)
            return
        # print("inner is ",type(inner))
        return inner
