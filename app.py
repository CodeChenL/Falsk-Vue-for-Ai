# 导入需要用到的库？or模块？
import os

from datetime import timedelta

from flask import Flask, Response, send_file, request


import json

# 创建一个Flask程序
app = Flask(__name__)


# 设置静态文件的过期时间，否则可能不能即使更新页面数据
app.send_file_max_age_default = timedelta(seconds=1)


# 浏览器访问"/"路径时，返回test2.html页面
@app.route('/')
def index():
    return send_file('static/test2.html')


# 浏览器请求"/json"时，相应json数据
@app.route('/json')
def data():
    # 设置要检索的路径
    path = "./static/img/"
    # 初始化要返回的json数据
    js = []
    # 初始化js[]数组的下标
    y = 0
    # 使用for循环遍历设置的路径下的文件夹,i为文件夹名
    for i in os.listdir(path):
        if i != "":
            # append方法可以向数组添加内容
            js.append(
                {
                    # 图片使用文件夹名进行分类，这里将i设置为对象的type属性
                    "type": i,
                    "img": []
                },
            )
            # 再循环遍历i文件夹内的图片文件，x为文件夹名
            for x in os.listdir(path + i):
                # 向刚刚向js数组添加的对象的img属性添加文件地址，js[y]为刚刚向js数组添加的对象，["img"]为此对象下的img属性
                if len(js[y]["img"]) <= 9:
                    js[y]["img"].append(
                        # 向js[y]对象下的img属性实为一个数组，添加文件的地址url
                        # 在flask框架里静态文件可以放在同目录下的static文件夹里，运行服务时可自动相应，无需再写路由
                        {"url": "/static/" + "img/" + i + "/" + x}
                    )
            # js的数组下标y的值+1
            y += 1
    # 以json数据格式返回js这个数组，json.dumps可将 Python 对象编码成 JSON 字符串，mimetype='application/json'可将json字符串转换成json数据
    return Response(json.dumps(js), mimetype='application/json')


# 当浏览器向“/uploader”发起请求时，使用GET，POST进行响应
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # 使变量f等于浏览器上传的文件列表
        f = request.files.getlist('file')
        # 循环遍历f，即浏览器上传的文件列表
        for file in f:
            # save方法可保存文件，，updir/为保存路径，filename为文件名
            file.save('updir/'+file.filename)
        # 返回文件上传成功的提示
        return '文件上传成功>_<'


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0"
    )
