import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sounddevice as sd

#音声ファイルのパス(相対)
audio_file_path = r'C:\Users\vecto\Desktop\python\get_vocal\少女レイ  MORE MORE JUMP  初音ミク_320kbps.mp3'
audio_file_path_offvo = r'C:\Users\vecto\Desktop\python\get_vocal\Shoujorei_offvocal_[Master].wav'

#音声データ読み込み
audio_data,sample_rate = librosa.load(audio_file_path)
audio_data_offvo,sample_offvo = librosa.load(audio_file_path_offvo)

#位相反転
inverted_audio_data_offvo = audio_data_offvo * (-1)

#波形チェック　終わり次第コメントアウト
off_time = np.arange(0,len(audio_data_offvo))/sample_offvo
#check_data = audio_data_offvo + inverted_audio_data_offvo
#plt.plot(off_time,check_data)

#plt.show()

#オフセットチェック
offset = 0

cross_correlation_coefficient = np.correlate(audio_data,audio_data_offvo,mode='valid')
        
offset = np.argmax(cross_correlation_coefficient)

#再生関数
def play(sampling_rate,audio_data):
    sd.play(audio_data,sampling_rate)
    sd.wait()


#ボーカル抽出
if len(audio_data)<len(audio_data_offvo):
    smaller_data = audio_data
    greater_data = audio_data_offvo
else:
    smaller_data = audio_data_offvo
    greater_data = audio_data

smaller_data = np.pad(smaller_data,(0,offset),mode='constant')
shifted_smaller_data = np.roll(smaller_data,offset)

#無理やり合わせる
n = abs(len(greater_data) - len(shifted_smaller_data))
shifted_smaller_data = np.pad(shifted_smaller_data,(0,n),mode='constant')

out_data = shifted_smaller_data + greater_data
play(sample_rate,out_data)

