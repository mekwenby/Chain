# Chain（链条）
基于Http协议用Flask模块实现的队列系统，可用于多台终端间建立生产消费队列。

主要用于分布式计算任务分发。



#### 快速开始：

下载代码，导入到项目

```python
# 导入用内存存储数据的Chain模块
from chain.memory import Chain
# 导入api模块
from apiserver import app
# 初始化Chain
c = Chain(lasting=True)         # lasting=True 打开数据持久化

'''设置lasting=True后所有的改动都将同步到 Chain.file 中'''

c.passwd = '000000'             # 设置密码

''' passwd 用于api清空队列 默认为 123456 '''

app.chain = c                   # 绑定到Flask 示例化对象

if __name__ == '__main__':
    # 运行Flask 示例
    app.run()
```



#### 用requests测试api：

```python
import requests

host = 'http://127.0.0.1:5000/'

# 获取队列长度
print(requests.get(url=host + 'len').json())

# 添加值到队列
for i in range(1000):
    data = {'string': f'YYY{i * 9 - 1}', 'abc': f'CCC{i * 9 + 1}'}
    print(requests.post(url=host + 'add', data=data).json())

# 获取一个值
print(requests.get(url=host + 'get').json())

# 清空队列
print(requests.post(url=host + 'clear', data={'passwd': '000000'}).json())

```



### plan（未来计划）：

##### 编写将数据存储到Redis的模块：

​	用于分布式部署api

##### 编写将数据存储到sqlite和mysql的模块:

​	方便嵌入到其他项目中
