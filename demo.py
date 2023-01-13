# 模块示例

from chain.memory import Chain
from apiserver import app

c = Chain(lasting=True)         # 持久化 开
c.passwd = '000000'             # 设置密码
app.chain = c                   # 绑定到Flask 示例化对象

if __name__ == '__main__':
    app.run()