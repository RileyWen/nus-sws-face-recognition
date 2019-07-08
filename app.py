from flask import Flask, request
import base64

app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


def base64_to_img(img):
    pass


@app.route('/UploadPic', methods=['POST'])
def process_img():
    img_b64 = request.form['image'].split(',')[1]

    print(img_b64)

    return 'received!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2333', debug=True)
