import numpy as np
import wave

def clip(data,sample_width,level=None,threshold=None,ratio=None,complex=None):
	if threshold==None:
		if sample_width==2:
			threshold=32767.0
		elif sample_width==4:
			threshold=2147483647.0
		
	if complex!=None:
		gain=1/(threshold+(1-threshold)*ratio)
		print(gain)
		#元の波形を圧縮
		data[data>threshold]=threshold+(data[data>threshold]-threshold)*ratio
		data[data<-threshold]=-threshold+(data[data<-threshold]+threshold)*ratio
		#増幅の余地を残してるため全体が増幅される
		data*=gain
	else:
		if data[data>threshold].shape[0]>1 or data[data<-threshold].shape[0]>1 :
			print("clipping")
			data[data>threshold]=threshold
			data[data<-threshold]=-threshold
			data*=level
		
	return data

def distortion(data,threshold,gain=100,level=0.5):
	data=data*gain
	data=clip(data,level,threshold)
	return 

def ring_modulation(data,depth=1,rate=1):
	n=np.arange(data.shape[0])
	y=depth*np.sin(2*np.pi*rate*n)
	mod=data*y
	return mod

def chorus(sr,data,depth,rate,time):
	d=sr*time #d(sec)
	depth=sr*depth
	n=np.arange(data.shape[0]).astype(np.float32)
	tau=d+depth*np.sin(2*np.pi*n*rate/sr) #d+-depth(msec)の範囲で揺らす
	t=n-tau
	m=t.astype(np.int32)
	delta=t-m.astype(np.float32)
	a=np.array(np.where(m>0))
	b=np.array(np.where(m+1<data.shape[0]))
	intersect=np.intersect1d(a,b)
	data[intersect]+=delta[intersect]*data[m[intersect]+1]+(1.0-delta[intersect])*data[m[intersect]]
	return data

def autpan(sr,depth,rate,n_sample,data):
		n=np.arange(n_sample)
		
		l_data=(1+depth*np.sin(2*np.pi*rate*n/sr))*data[0::2]
		r_data=(1-depth*np.sin(2*np.pi*rate*n/sr))*data[1::2]
		c=altanative_connect(l_data,r_data)		
		return c
def altanative_connect(n_sample,data,l_data,r_data):
	data=np.arange(n_sample)
	return np.insert(r_data,data,l_data)

#適正a 0.7~0.1
#適正ディレイ0.35~0.7
def delay(data,sr=None,delay=0.35,rep=2,a=0.5):
	if sr==None:
		sr=44100
	delay*=sr 
	for i in range(data.shape[0]):	
		for n in range(1,rep):
			m=int(i-n*delay)
			if m>=0:
				data[i]+=pow(a,n)*data[m]

def load(path=None,sr=None,all=None,size=None):
	if path==None:
		raise Exception("path is not found")
	else:
		with wave.open(path,"rb") as file:
			if size==None:
				n_sample=file.getnframes()
			else:
				n_sample=size
					
			if sr==None:
				sr=file.getframerate()
			else:
				sr=sr
				
			channels=file.getnchannels()
			sample_width=file.getsampwidth()
			buf=file.readframes(n_sample)
			
		#record_time=n_sample/sr
		if sample_width==2:
			data=np.frombuffer(buf,dtype='int16')
			data=data/32768.0
		else:
			sample_width==4
			data=np.frombuffer(buf,dtype='int32')
			data=data/2147483648.0
		
		if channels==2:
			#l_channel=data[0::2]
			#r_channel=data[1::2]
			#データ解析時はデータ数を減らすのを推奨
			#all==None :default
			if all==None:
				data=data[0::2]
		del buf
		return np.array(data),sr
