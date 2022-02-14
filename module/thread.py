import threading
from .SoundIO import SoundIO

class Threading_record(threading.Thread):

    def __init__(self,q,play_flag,data_flag,vol_level,play_stop_flag,daemon):
        super(Threading_record,self).__init__()
        self.q=q
        self.daemon=daemon
        
        self.vol_level=vol_level
        self.data_flag=data_flag
        self.play_flag=play_flag
        self.play_stop_flag=play_stop_flag
    
    def run(self):
        r=SoundIO(self.q,self.play_flag,self.data_flag,self.vol_level,self.play_stop_flag)
        r.run()