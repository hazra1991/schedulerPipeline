from multiprocessing import Process
from threading import Thread


def fun():
    import time
    import os
    print(os.getpid(),"    ",os.getppid())
    time.sleep(60)
    print('fun ran ')



t1 = Thread(target= fun).start()
t2 = Thread(target= fun).start()
t3 = Thread(target= fun).start()
t4 = Thread(target= fun).start()
t5 = Thread(target= fun).start()

# t1 = Process(target= fun).start()
# t2 = Process(target= fun).start()
# t3 = Process(target= fun).start()
# t4 = Process(target= fun).start()
# t5 = Process(target= fun,daemon=True)
# t5.start()
# t1.start()
# t5.join()
print("this is running ")