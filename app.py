from flask import Flask, request
import base64
from ibm_watson import VisualRecognitionV3
import json
import cv2 as cv

visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey='LEzLPAGHwS9dPAzZytHjUQ7xxYifVETSBF5IviM_t03R')

app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


def add_frame_on_face(faces):
    img = cv.imread('img_tmp/img')

    # print(faces)

    for face in faces:
        location = face['face_location']
        x1 = location['left']
        y1 = location['top']
        x2 = x1 + location['width']
        y2 = y1 + location['height']
        cv.rectangle(img, (x1, y1), (x2, y2), (48, 185, 98), 2)

    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


@app.route('/UploadPic', methods=['POST'])
def process_img():
    img_b64 = request.form['image'].split(',')[1]
    img = base64.b64decode(img_b64)

    with open('img_tmp/img', 'wb') as file:
        file.write(img)

    with open('img_tmp/img', 'rb') as file:
        result = visual_recognition.detect_faces(file).get_result()
        pass

    # print(json.dumps(result, indent=2))

    faces = result['images'][0]['faces']
    # Notice that we upload only one image
    add_frame_on_face(faces)

    return 'received!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2333', debug=True)
