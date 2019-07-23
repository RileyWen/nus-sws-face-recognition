# Subtitler - A Fast & Convenient Subtitle Generator

## Runtime Environment Configuration

1. Apply an Google Cloud Platform account
2. Create a project and enable two API:
    - Cloud Speech-to-Text API
    - Cloud Translation API
3. Get the credential of the project service account (in json format)
4. Set up the **python 3** virtual environment
    - Under Linux, it can be `python3 -m venv ./venv`
5. Enter the virtual environment and run `pip install -r requirements.txt`
6. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of json file in **Step 3**
    - Under Linux it can be `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credential.json`
7. Create a directory `img_tmp` under the root of the project.
8. run `python app.py` to start the server