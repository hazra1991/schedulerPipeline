from .utils import consume,produce

class Manager:
    def __init__(self,**kwargs):
        self._jobmapper = dict()
        self.__workerlist = []
        self.__workerstatus = False
        self.__MQServer = kwargs.get('host','localhost')

    def register(self,*arg):
        for fun in arg:
            self._jobmapper.setdefault(fun.__name__,fun)
    
    def startworker(self,max_workers=4,multiprocessing = False):
        if self.__workerstatus:
            self.stop()
            raise RuntimeError('[*] Worker already scheduled for the object')
        self.__workerstatus = True
        if multiprocessing:
            from multiprocessing import Process,Lock
            lock = Lock()
            for num in range(max_workers):
                p = Process(target=consume,args=(self,self.__MQServer,num,lock))
                self.__workerlist.append(p)
                p.start()
        else:
            from threading import Thread ,Lock
            lock = Lock()
            for num in range(max_workers):
                p = Thread(target=consume,args=(self,self.__MQServer,num,lock))
                self.__workerlist.append(p)
                p.start()

        print("this is printing")

    def registerAndPublishJob(self,fun,*args,**kwargs):
        self._jobmapper.setdefault(fun.__name__,fun)
        self.publishJob(fun.__name__,*args,**kwargs)
    
    def publishJob(self,funname,*args,**kw):
        if not self._jobmapper.get(funname):
            raise ValueError(f'{funname} Job not registered')
        produce(self.__MQServer,funname,*args,**kw)


    def join(self):
        ''' blocking call ''' 
        if not self.__workerlist:
            raise ValueError('No workers available')
        for worker in self.__workerlist:
            worker.join()
        return True
        
            
    def stop(self):
        print("[*] Stoping all execution")
        for worker in self.__workerlist:
            if worker.is_alive:
                worker.terminate()

