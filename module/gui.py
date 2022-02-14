import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.animation as animation
import numpy as np
import sys
from tkinter import font
import wave 
import time
from .sound_process import clip,load

class GUI(object):
    
    def __init__(self,q,play_flag,data_flag,vol_level,play_stop_flag):
        
        self.fetch_file=None
        self.sr=44100
        self.record_f=2
        self.wave_data=np.zeros(self.sr*3//32)
        self.data=np.array([])
        self.play_flag=play_flag
        self.data_flag=data_flag
        self.q=q
        self.wav_data=np.array([])
        self.vol=vol_level
        self.play_stop_flag=play_stop_flag

        #GUI設定
        self.root = tkinter.Tk()
        self.root.resizable(width=False, height=False)
        self.root.wm_title("Visual waveform")
        self.root.wm_geometry("1800x500")
        frame_icon='img/app.ico'
        self.root.iconbitmap(default=frame_icon)
        

        self.build_menue()
        self.build_tool_buttom()
        self.graph_pack()

    def run(self):
        l = np.arange(0, 80, 0.01)  
        ani=animation.FuncAnimation(self.fig1, self.animate, l,
            init_func=self.init, interval=52, blit=True,)
        self.fft_area.get_tk_widget().pack()
        tkinter.mainloop()
        
    #システムを強制終了
    def _quit(self):
        self.root.quit()     
        self.root.destroy()
        time.sleep(1)
        sys.exit()
    
    #ファイルを開く
    def open_file(self):
        filename = filedialog.askopenfilename()
        self.fetch_file=filename
        print(self.fetch_file[-3:])
        if self.fetch_file[-3:]=="wav":
            self.wav_data,self.wav_sr=load(self.fetch_file)

    #アプリ終了
    def close_disp(self):
        self._quit()


    #メニュー設定
    def build_menue(self):
        menue = tkinter.Menu(self.root,bg="black")
        self.root.config(menu=menue)
        menu_file = tkinter.Menu(menue,tearoff=0) 
        menue.add_cascade(label='ファイル', menu=menu_file) 
        menu_file.add_command(label='開く', command=self.open_file, accelerator="Ctrl+O") 
        menu_file.add_command(label='名前を付けて保存', command=self.save_data,accelerator="Ctrl+S")
        menu_file.add_separator()
        menu_file.add_command(label='終了', command=self.close_disp)
        menu_edit = tkinter.Menu(menue,tearoff=0)
        menue.add_cascade(label='ヘルプ', menu=menu_edit)
        menu_edit.add_command(label='バージョン情報', command=self.version_info)

    #toolボタン作成
    def build_tool_buttom(self):
        tool_buttom=tkinter.Frame(self.root, borderwidth = 2, relief = tkinter.SUNKEN)
        tool_buttom.place(relx=0.6, rely=0.6)
        button1 =tkinter.Button(tool_buttom, text = "録音", width = 8,height=2,command=self.record_push)
        button2 =tkinter.Button(tool_buttom, text = "録音停止", width = 8,height=2,command=self.record_stop_push)
        button3 =tkinter.Button(tool_buttom, text = "削除", width = 8,height=2,command=self.clear_push)
        button4 =tkinter.Button(tool_buttom, text = "初めから再生", width = 8,height=2,command=self.restart)
        button5 =tkinter.Button(tool_buttom, text = "再生", width = 8,height=2,command=self.play_push)
        button6 =tkinter.Button(tool_buttom, text = "再生中止", width = 8,height=2,command=self.play_cancel)
        button7 =tkinter.Button(tool_buttom, text = "再生停止", width = 8,height=2,command=self.play_stop)
        font1 = font.Font(family='Helvetica', size=14)
        text=tkinter.Label(tool_buttom,text="録音音量",font=font1)
        self.scale_var = tkinter.DoubleVar()
        sound_scale = tkinter.Scale(tool_buttom,
                        variable = self.scale_var, 
                        command = self.slider_scroll,
                        orient=tkinter.HORIZONTAL,   
                        length=300,           
                        width=20,            
                        sliderlength=20,      
                        from_=0.1,            
                        to=10,               
                        resolution=0.5,       
                        tickinterval=0
                        )
        #text2=tkinter.Label(tool_buttom,text="読み込みファイル",font=font1)
        #file_text=tkinter.Label(tool_buttom,text="NULL",font=font1)
        #button8 =tkinter.Button(tool_buttom, text = "wav再生", width = 8,height=2,command=self.play_wav)

        button1.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button2.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button3.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button4.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button5.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button6.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        button7.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        text.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        sound_scale.pack(side = tkinter.LEFT,fill=tkinter.NONE,padx=2,pady=1)
        #text2.pack(side = tkinter.RIGHT,fill=tkinter.NONE,padx=2,pady=1)
        #file_text.pack(side = tkinter.RIGHT,fill=tkinter.NONE,padx=2,pady=1)
        #button8.pack(side = tkinter.RIGHT,fill=tkinter.NONE,padx=2,pady=1)
        
        tool_buttom.pack(fill = tkinter.X)

    """
    def play_wav(self):
        self.play_wav.value=1
    """
    def restart(self):
        self.play_flag.value=3
    def play_cancel(self):
        self.play_flag.value=4

    #録音データと表示用データを削除
    def clear_push(self):
        #再生途中で削除は行わない(-1で再生途中)
        if self.play_flag.value!=-1:
            self.wave_data=np.zeros(self.sr*3//32)
            self.data=np.array([])
            self.data_flag.value=1
        
    #スライドバーの設定
    def slider_scroll(self, event=None):
        self.vol.value=self.scale_var.get()

    #ファイル保存関数
    def save_data(self):
        if self.data.shape[0]!=0:
            filename = filedialog.asksaveasfilename(title = "名前を付けて保存",
                filetypes = [("Wav", ".wav")], # ファイルフィルタ
                initialdir = "./", # 自分自身のディレクトリ
                defaultextension = "wav"
                )

            #self.data=clip(self.data,2,1).astype("int16")
            with wave.open(filename, 'w') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)
                f.writeframes(self.data.astype("int16"))
        else:
            self.sub_win = tkinter.Toplevel()
            self.sub_win.wm_title("Error")
            self.sub_win.geometry("200x100")
            font1 = font.Font(size=8)
            label = tkinter.Label(self.sub_win,text="保存するデータがありません。",font=font1)
            label.pack()
            button =tkinter.Button(self.sub_win, text = "OK", width = 10,height=2,command=self.close)
            button.pack(side=tkinter.BOTTOM,pady=2)
            self.sub_win.grab_set()

    def version_info(self):
        self.sub_win = tkinter.Toplevel()
        self.sub_win.wm_title("バージョン情報")
        self.sub_win.geometry("400x400")
        font1 = font.Font(size=18)
        font2 = font.Font(size=12)
        label = tkinter.Label(self.sub_win,text="\nバージョン情報\n\n\n\n",font=font1)
        label.pack()
        label_sub = tkinter.Label(self.sub_win,text="バージョン:1.1\n最終更新日時:2022/02/14\nDevelopment environment:Windows 10\nimport Package:\nPyaudio==0.2.11\nmatplotlib==3.3.4\nnumpy==1.20.1",font=font2)
        label_sub.pack()
        button =tkinter.Button(self.sub_win, text = "OK", width = 16,height=2,command=self.close)
        button.pack(side=tkinter.BOTTOM,pady=2)
        self.sub_win.grab_set()

    #サブウインドウを閉じる
    def close(self):
        self.sub_win.destroy()
        
    def record_push(self):
        #再生途中で録音は行わない(-1で再生途中)
        if self.play_flag.value!=-1:
            while self.q.qsize()>0:
                self.q.get()
            self.record_f=1
            self.play_flag.value=1


    
    def play_stop(self):
        if self.play_flag.value==2:
            self.play_stop_flag.value=1

    def record_stop_push(self):
        #再生途中で録音停止は行わない(-1で再生途中)
        if self.play_flag.value!=-1:
            while self.q.qsize()>0:
                self.q.get()
            self.record_f=2
            self.play_flag.value=0
    #再生
    def play_push(self):
        self.record_f=3
        self.play_flag.value=2

    def graph_pack(self):
        self.wave_plot_graph()
        self.fft_plot_graph()

    #FFTグラフ設定
    def fft_plot_graph(self):
        self.fig1,self.ax1= plt.subplots(figsize=(8,4),dpi=100) 
        self.fft_area = FigureCanvasTkAgg(self.fig1, master=self.root)
        self.fft_area.get_tk_widget().pack(side=tkinter.LEFT,anchor=tkinter.N)
        self.fig1.patch.set_alpha(0.5)
        self.ax1.patch.set_facecolor('black')
        self.ax1.set_ylim([-10, 400])
        self.ax1.set_xlabel("Hz")
        self.line1, = self.ax1.plot(np.linspace(0, 5000, 238),np.zeros(238),c="white")
    #波形グラフ設定
    def wave_plot_graph(self):
        self.fig2,self.ax2= plt.subplots(figsize=(10,4),dpi=100) 
        self.wave_area = FigureCanvasTkAgg(self.fig2, master=self.root)
        self.wave_area.get_tk_widget().pack(side=tkinter.LEFT,anchor=tkinter.N)
        self.fig2.patch.set_alpha(0.5)
        self.ax2.patch.set_facecolor('black')
        self.ax2.set_ylim([-1, 1])
        self.ax2.tick_params(labelbottom=False,bottom=False,)
        self.fig2.subplots_adjust(left=0.1, right=1)
        self.line2, = self.ax2.plot(np.linspace(-5, 0, self.sr*3//32),self.wave_data,c="white")
    
    def init(self): 
        self.line1.set_ydata(np.zeros(238))
        self.line2.set_ydata(np.zeros(self.sr*3//32))
        return self.line1,self.line2

    def animate(self,_):
        if self.record_f==1:
            #録音しているときはFFT更新しない。処理が重くなる。
            if self.q.qsize()>0:
                x=self.q.get()
                y=np.frombuffer(x, dtype=np.int16)
                self.data=np.append(self.data,y*self.vol.value)
                #表示用は間引いたデータ使う＜＝重くなるから
                data=y[0::64]*0.001
                self.wave_data=self.wave_data[len(data):]
                self.wave_data=np.concatenate([self.wave_data,data],0)
                self.line2.set_ydata(self.wave_data)
                # 遅延対策のためキューのデータを捨てる
                if self.q.qsize()>0:
                    x=self.q.get()
                    y=np.frombuffer(x, dtype=np.int16)
                    self.data=np.append(self.data,y*self.vol.value)
                    #print(self.q.qsize())
            return self.line2,
        else:
            #録音していないときはFFT表示
            if self.q.qsize()>0:
                x=np.frombuffer(self.q.get(), dtype=np.int16)
                h=np.hanning(2024)
                sp=np.abs(np.fft.fft(x*h)[:238])
                self.line1.set_ydata(sp*0.001)
                
                # 遅延対策のためキューのデータを捨てる
                if self.q.qsize()>3:
                    self.q.get()
            return self.line1,
        
        

    