import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import PySimpleGUI as sg

#音声ファイルパス
on_audio_path = r'C:\Users\vecto\Desktop\python\music_data\みきとP 『 少女レイ 』 MV .wav'
off_audio_path = r'C:\Users\vecto\Desktop\python\music_data\Shoujorei_offvocal_[Master].wav'

#音声データ読み込み
on_audio_data,on_sample_rate = librosa.load(on_audio_path)
off_audio_data,off_sample_rate = librosa.load(off_audio_path)
                                       
#調整用変数
offset = 0
audio_sum = 0
audio_test = 0
volume_rate_c = 0.1

#音声長２
length = min(len(on_audio_data),len(off_audio_data))
if(len(on_audio_data)<len(off_audio_data)):
    off_audio_data = off_audio_data[:length]
else:
    on_audio_data = on_audio_data[:length]

#gui表示
layout = [[sg.Text("set range for offset[sample]")],
          [sg.Input(key = 'range_offset')],
          [sg.Text("set base for volume[sample]")],
          [sg.Input(key='base')],
          [sg.Text("set range for volume[sample]")],
          [sg.Input(key = 'range_volume')],
          [sg.Button('Go')]]

window = sg.Window('Get Vocal',layout)
#event_loop
while True:
    event, values = window.read()

    if event == 'Go':

        #オフセット
        on_audio_data = np.pad(on_audio_data,(int(values['range_offset']),int(values['range_offset'])),mode = 'constant')
        ccc = np.correlate(on_audio_data,off_audio_data,mode='valid')
        offset = np.argmax(ccc)
        off_audio_data = np.pad(off_audio_data,(offset,len(on_audio_data)-offset-len(off_audio_data)),mode = 'constant')

        #位相反転
        inverted_off_audio_data = off_audio_data * (-1)

        #ボリューム
        for t in range(int(values['base'])-int(values['range_volume']),int(values['base'])+int(values['range_volume'])+1):
            audio_sum += on_audio_data[t] + inverted_off_audio_data[t] * 0.1
        for volume_rate in range(2,21):
            volume_rate = volume_rate / 10
            for t in range(int(values['base'])-int(values['range_volume']),int(values['base'])+int(values['range_volume'])+1):
                audio_test += on_audio_data[t] + inverted_off_audio_data[t] * volume_rate
            if audio_sum > audio_test:
                audio_sum = audio_test
                volume_rate_c = volume_rate

        print('check1')

        #ボーカル抽出
        sum_audio_data = on_audio_data + inverted_off_audio_data
        sf.write('output.wav',sum_audio_data,on_sample_rate)

        print('check2')

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
        break
