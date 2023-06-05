import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
print('ok1')
#音声ファイルパス
on_audio_path = r'C:\Users\vecto\Desktop\python\music_data\みきとP 『 少女レイ 』 MV .wav'
off_audio_path = r'C:\Users\vecto\Desktop\python\music_data\Shoujorei_offvocal_[Master].wav'
print('ok2')
#音声データ読み込み
on_audio_data,on_sample_rate = librosa.load(on_audio_path)
off_audio_data,off_sample_rate = librosa.load(off_audio_path)
print('ok3')                                        

print('ok4')
#オフセット1
offset = 0
#ccc = np.correlate(on_audio_data, #off_audio_data, mode='valid')
#offset = np.argmax(ccc)

#音声長1
#if len(on_audio_data)<len(off_audio_data):
    #long_audio_data = inverted_off_audio_data
    #small_audio_data = on_audio_data
    #small_sample_rate = on_sample_rate
#else:
    #long_audio_data = on_audio_data
    #long_sample_rate = on_sample_rate
    #small_audio_data = inverted_off_audio_data
    #small_sample_rate = off_sample_rate

#音声長２
length = min(len(on_audio_data),len(off_audio_data))
if(len(on_audio_data)<len(off_audio_data)):
    off_audio_data = off_audio_data[:length]
else:
    on_audio_data = on_audio_data[:length]

print('ok5')
#オフセット探索用パディング



print(on_sample_rate)
#オフセット２
on_audio_data = np.pad(on_audio_data,(5000,5000),mode = 'constant')
ccc = np.correlate(on_audio_data,off_audio_data,mode='valid')
offset = np.argmax(ccc)
off_audio_data = np.pad(off_audio_data,(offset,len(on_audio_data)-offset-len(off_audio_data)),mode = 'constant')


#音声長とオフセットを調節1
#small_audio_data = np.pad(small_audio_data,(0,offset),mode='constant')
#small_audio_data = np.roll(small_audio_data,offset)
   #xxooox
   #ooo
   #↓
   #xxooox
   #xxooo
#n = abs(len(long_audio_data)-len(small_audio_data))
#small_audio_data = np.pad(small_audio_data,(0,n),mode='constant')
   #↓
   #xxooox

#位相反転
inverted_off_audio_data = off_audio_data * (-1)

#ボーカル抽出
sum_audio_data = on_audio_data + inverted_off_audio_data
sf.write('output.wav',sum_audio_data,on_sample_rate)

###########以下デバッグ############
#位相反転チェック
#invertion_check_audio_data = inverted_off_audio_data + off_audio_data
#sf.write('invertion_check.wav',invertion_check_audio_data,off_sample_rate)

#データ出力
sf.write('inverted_off_audio_data.wav',inverted_off_audio_data,off_sample_rate)
sf.write('off_audio_data.wav',off_audio_data,off_sample_rate)
sf.write('on_audio_data.wav',on_audio_data,on_sample_rate)
print('ok6')
#音声長チェック
if len(on_audio_data) == len(off_audio_data):
    print('ok')
if len(on_audio_data) == len(inverted_off_audio_data):
    print('okdesu')