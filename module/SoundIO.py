
import numpy as np
import struct
import pyaudio
import time

class SoundIO():
    def __init__(self,q,play_flag,data_flag,vol_level,play_stop_flag):
        self.RATE=44100
        self.CHUNK=2024
        self.FORMAT = pyaudio.paInt16
        self.p=pyaudio.PyAudio()
        self.q=q
        self.data_flag=data_flag
        self.play_stop_flag=play_stop_flag
        self.vol_level=vol_level
        self.a=np.array([])
        self.play_flag=play_flag
        self.stream=self.p.open(format =self.FORMAT,
                channels = 1,
                rate = self.RATE,
                frames_per_buffer = self.CHUNK,
                input = True,
                output = True)
        
    def run(self):
        
        try:
            while self.stream.is_active():
                
                #通常時
                if self.play_flag.value==0:
                    data = self.stream.read(self.CHUNK)
                    self.q.put(data)
                    
                #録音時
                elif self.play_flag.value==1:
                    data = self.stream.read(self.CHUNK)
                    y=(np.frombuffer(data, dtype=np.int16)*self.vol_level.value).astype(np.int16)
                    y = struct.pack("h" * len(y), *y)
                    self.q.put(data)
                    self.a=np.append(self.a,y)
                #録音再生時
                else:
                    c=0
                    while c<len(self.a):
                        if self.play_stop_flag.value==1:
                            self.play_flag.value=-1
                            #停止ボタンで無限ループ待機を発生させる
                            while self.play_flag.value!=2:
                                pass
                            self.play_stop_flag.value=0
                        
                        if self.play_flag.value==4:
                            c+=10000
                            #音源の領域を超えたらブレイク
                            if len(self.a)<c:
                                self.play_flag.value=2
                                break
                       
                        elif self.play_flag.value==3:
                            c=0
                            self.play_flag.value=2
                        self.stream.write(self.a[c])
                        c+=1
                    self.play_flag.value=0
                    self.play_stop_flag.value=0
                
                    

                if self.data_flag.value==1:
                    self.a=np.array([])
                    self.data_flag.value=0 
                
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        except SystemExit:
            print("SystemExit")
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()