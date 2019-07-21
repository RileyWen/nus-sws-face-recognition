from flask import Flask, request
import base64
import re
import io
import json
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3beta1 as translate

app = Flask(__name__, static_url_path='')


def resp_to_sentence_ts(response):
    ts_list = []
    sentence_list = []
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        # 以句号，问号，感叹号分割文本
        s_list = re.split(r'(\. |。 |？ |\? |! |\.$|。$|？$|\?$|!$)', transcript)
        print(s_list)
        # 将标点符号连接到句子
        j = 1
        while j < len(s_list):
            if s_list[j] in ['.', '。', '?', '？', '!', '！', '. ', '。 ', '? ', '？ ', '! ', '！ ']:
                s_list[j - 1] += s_list[j]
                s_list.pop(j)
            else:
                j = j + 1
        if '' in s_list:
            s_list.remove('')
        # ssentence_list为原始句子list
        for s in s_list:
            sentence_list.append(s)

        count_begin = 0
        count_end = -1
        word_list = []
        for word_info in alternative.words:
            word_list.append(word_info)
            pass
        for sentence in s_list:
            word = sentence.split(' ')
            if '' in word:
                word.remove('')

            count_begin = count_end + 1
            count_end = count_begin + len(word) - 1  # - punctuation_cnt

            begin_time = word_list[count_begin].start_time.seconds + word_list[count_begin].start_time.nanos * 1e-9
            end_time = word_list[count_end].end_time.seconds + word_list[count_end].end_time.nanos * 1e-9
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
            time = bh + ':' + bm + ':' + bs + ',' + bms + ' --> ' + eh + ':' + em + ':' + es + ',' + ems
            ts_list.append(time)
            pass

    for i in range(0, len(sentence_list)):
        sentence_list[i] = sentence_list[i].lstrip()
    # 返回的sentence_list为句子list， ts_list为时间戳list
    return sentence_list, ts_list


def google_translate(text_list_to_translate: list):
    client = translate.TranslationServiceClient()
    project_id = 'moycat'

    # project_id = YOUR_PROJECT_ID
    # text = 'Text you wish to translate'
    location = 'global'

    parent = client.location_path(project_id, location)

    response = client.translate_text(
        parent=parent,
        contents=text_list_to_translate,
        # contents=['This is a Test!', 'This is my name?'],
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en-US',
        target_language_code='zh-CN')

    translate_text_list = []
    for translation in response.translations:
        # print('Translated Text: {}'.format(translation.translate_text_list))
        translate_text_list.append(translation.translated_text)
    print(translate_text_list)

    return translate_text_list


def srtformatter(translate_list, s_list, ts_list):
    srt = ''
    for i in range(len(s_list)):
        srt += str(i + 1) + '\n' + ts_list[i] + '\n' + s_list[i] + '\n' + translate_list[i] + '\n\n'
    return srt


def print_voice_recognition_result(response):
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        words_info = result.alternatives[0].words

        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))

        for word_info in words_info:
            start_time = word_info.start_time
            end_time = word_info.end_time
            # print("word: '{}', speaker_tag: {}, ".format(word_info.word,
            #                                              word_info.speaker_tag),
            #       end='')
            print("word: '{}', ".format(word_info.word), end='')
            print('start_time: {}, end_time: {}'.format(
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))


def google_voice_recognition(speech_file: str):
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        use_enhanced=True,
        model='video',
        # enable_speaker_diarization=True,
        # diarization_speaker_count=5
    )

    response = client.recognize(config, audio)

    print_voice_recognition_result(response)

    sentence_list, ts_list = resp_to_sentence_ts(response)

    translate_text_list = google_translate(sentence_list)

    srt = srtformatter(translate_text_list, sentence_list, ts_list)

    print(sentence_list)
    print(ts_list)
    print(translate_text_list)

    srt_b64 = base64.b64encode(srt.encode("utf-8")).decode("utf-8")
    print(srt_b64)
    return srt_b64


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


DEBUG = False


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

    return srt


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2333')
