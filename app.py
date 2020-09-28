import os

from datetime import timedelta

from flask import Flask, render_template, Response, request

from werkzeug.utils import secure_filename

import json

app = Flask(__name__)

app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/')
def index():
    return render_template('test2.html')


@app.route('/json')
def data():
    path = "C:/Users/PC/Desktop/FlaskWebForAi/static/img/"
    js = []
    y = 0
    for i in os.listdir(path):
        if i != "":
            js.append(
                {
                    "type": i,
                    "img": []
                },
            )
            for x in os.listdir(path + i):
                js[y]["img"].append(
                    {"url": "/static/" + "img/" + i + "/" + x}
                )
            y += 1

    return Response(json.dumps(js), mimetype='application/json')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files.getlist('file')
        for file in f:
            file.save(os.path.join('updir/', secure_filename(file.filename)))
        return '文件上传成功>_<'


if __name__ == "__main__":
    app.run()
