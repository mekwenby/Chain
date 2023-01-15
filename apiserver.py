from flask import Flask, jsonify, request

'''分布式添加 or 获取队列API'''

app = Flask(__name__)

'''为app绑定chain'''
app.chain = None
app.apiversion = 'v1.1-920'


@app.route('/')
def hello_world():
    """返回信息"""

    dic = {
        'version': app.chain.version,
        'apiversion': app.apiversion,
        'len': app.chain.len(),
    }

    return jsonify(dic)


@app.route('/add', methods=['POST', 'GET'])
def add():
    """添加到队列,任意 key，v 只取 v """
    if request.method == 'POST':
        '''POST方式添加队列'''
        # 优化为批量添加
        app.chain.adds(request.form.values())
        return jsonify(app.chain.len())

    elif request.method == 'GET':
        '''GET方式添加队列'''
        app.chain.adds(request.args.values())
        return jsonify(app.chain.len())

    else:
        return jsonify('Fail!')


@app.route('/get')
def get():
    """从队列中获取一个值"""
    return jsonify(app.chain.get())


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        '''POST方式删除'''
        # 优化为批量添加

        return jsonify(app.chain.deletes(request.form.values()))

    elif request.method == 'GET':
        '''GET方式删除'''
        return jsonify(app.chain.deletes(request.args.values()))

    else:
        return jsonify('Fail!')


@app.route('/len')
def len():
    """获取队列长度"""
    return jsonify(app.chain.len())


@app.route('/clear', methods=['POST'])
def clear():
    """清空队列，需要传Chain的passwd,keys为passwd"""
    if request.method == 'POST':
        passwd = request.form.get('passwd')
        if passwd == app.chain.passwd:
            app.chain.clear()
            return jsonify('Pass!')
        else:
            return jsonify('Fail!')
