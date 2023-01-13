from flask import Flask, jsonify, request

'''分布式添加 or 获取队列API'''

app = Flask(__name__)

'''为app绑定chain'''
app.chain = None


@app.route('/')
def hello_world():
    """返回版本号"""
    return jsonify(app.chain.version)


@app.route('/add', methods=['POST'])
def add():
    """添加到队列，POST请求,任意 key，v 只取 v """
    if request.method == 'POST':

        '''for s in request.form.values():

            if s is not None:
                app.chain.add(s)'''
        # 优化为批量添加
        app.chain.adds(request.form.values())
        return jsonify(app.chain.len())

    else:
        return jsonify(0)


@app.route('/get')
def get():
    """从队列中获取一个值"""
    return jsonify(app.chain.get())


@app.route('/len')
def len():
    """获取队列长度"""
    return jsonify(app.chain.len())


@app.route('/clear', methods=['POST'])
def clear():
    """清空队列，需要传一个密码"""
    if request.method == 'POST':
        passwd = request.form.get('passwd')
        if passwd == app.chain.passwd:
            app.chain.clear()
            return jsonify('Pass!')
        else:
            return jsonify('Fail!')
