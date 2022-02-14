from multiprocessing.dummy import Array
from xmlrpc.client import boolean
from module import gui,thread
import queue
from multiprocessing import Value
if __name__ == '__main__':
    q = queue.Queue()
    
    play_flag=Value('i',0)
    data_flag=Value('i',0)
    play_stop_flag=Value('i',0)
    vol_level=Value('f',1)
    t1 = thread.Threading_record(q,play_flag,data_flag,vol_level,play_stop_flag,daemon=True)
    t1.start()
    gui=gui.GUI(q,play_flag,data_flag,vol_level,play_stop_flag)
    gui.run()

