from flask import Flask, request
import base64
import re
import io
import json
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3beta1 as translate

app = Flask(__name__, static_url_path='')


def srtformatter(response):
    num = 1
    srt = ''
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        # 以句号，问号，感叹号分割文本
        s_list = re.split('[，,.。？?!]', transcript.strip())

        count_begin = 0
        count_end = -1
        word_list = []
        for word_info in alternative.words:
            word_list.append(word_info)
            pass
        for sentence in s_list:
            word = sentence.split(' ')
            if sentence != '':
                if '' in word:
                    word.remove('')
                count_begin = count_end + 1
                count_end = count_begin + len(word) - 1
                begin_time = word_list[count_begin].start_time.seconds + word_list[count_begin].start_time.nanos * 1e-9
                end_time = word_list[count_end].start_time.seconds + word_list[count_end].start_time.nanos * 1e-9
                begin_h = int(begin_time // 3600)
                bh = "{:0>2d}".format(begin_h)
                begin_m = int((begin_time - 3600 * begin_h) // 60)
                bm = "{:0>2d}".format(begin_m)
                begin_s = int(begin_time - 3600 * begin_h - 60 * begin_m)
                bs = "{:0>2d}".format(begin_s)
                begin_ms = begin_time - int(begin_time)
                bms = "{:.3f}".format(begin_ms)[2:]
                end_h = int(end_time // 3600)
                eh = "{:0>2d}".format(end_h)
                end_m = int((end_time - 3600 * end_h) // 60)
                em = "{:0>2d}".format(end_m)
                end_s = int(end_time - 3600 * end_h - 60 * end_m)
                es = "{:0>2d}".format(end_s)
                end_ms = end_time - int(end_time)
                ems = "{:.3f}".format(end_ms)[2:]
                time = bh + ':' + bm + ':' + bs + ',' + bms + ' --> ' + eh + ':' + em + ':' + es + ',' + ems + '\n'
                srt += str(num) + '\n' + time + sentence + '\n\n'
                num = num + 1
                pass
    return srt


def google_voice_recognition(speech_file: str):
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True, enable_word_time_offsets=True)

    response = client.recognize(config, audio)
    srt = srtformatter(response)
    return srt


def google_translate(text_list_to_translate: list):
    client = translate.TranslationServiceClient()
    project_id = 'ivory-honor-230713'

    # project_id = YOUR_PROJECT_ID
    # text = 'Text you wish to translate'
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.translate_text(
        parent=parent,
        contents=['This is a Test!', 'This is my name?'],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en-US',
        target_language_code='zh-CN')

    translated_text = []
    for translation in response.translations:
        # print('Translated Text: {}'.format(translation.translated_text))
        translated_text.append(translation.translated_text)
        print(translated_text)


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


DEBUG = True


@app.route('/UploadAudio', methods=['POST'])
def process_img():
    # print(request.form['image'])
    audio_path = 'img_tmp/audio'

    request_split = request.form['file'].split(',')
    audio_url_header = 'base64,'  # request_split[0]
    audio_b64 = request_split[1]
    audio = base64.b64decode(audio_b64)

    with open(audio_path, 'wb') as file:
        file.write(audio)

    if DEBUG:
        with open('C:\\Users\\riley\\Desktop\\NUS-SWS\\SWS3004 - Cloud Computing\\1_minute_video.srt') as file:
            srt = file.read()

        import time
        time.sleep(2)
    else:
        srt = google_voice_recognition(audio_path)

    google_translate([])
    return srt


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2333')
