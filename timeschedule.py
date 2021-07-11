# import pytz
# from datetime import datetime


# utcnow = datetime.now(pytz.utc)

# tz_info = pytz.timezone('Pacific/Midway')


# local = tz_info.localize(datetime.now())

# utc = local.astimezone(pytz.utc)

def fun(val):
    d = test(val)
    print(d.val)
    print(id(d))
    # return d


def run():
    for i in range(2):
        t = Process(target=fun,args=(i,))
        t.start
        t.start()


class test:
     def __init__(self):
            self.d = Manager().dict()
     def run(self):
            from multiprocessing import Process
            for i in range(3):
                t = Process(target=fun,args=(self,))
                t.start()


