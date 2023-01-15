# Chain（链条）
基于Http协议用Flask模块实现的队列系统，可用于多台终端间建立生产消费队列。

主要用于分布式计算任务分发。



#### 支持数据类型

- 字符串
- 整数
- 浮点数
- 布尔
- JSON



#### 通过Code使用Chain：

下载代码

导入到项目

安装依赖

###### 使用内存存储数据的chain: <demo>

```python
from apiserver import app
from chain import Memory,Redis

app = app
app.chain = Memory()


if __name__ == '__main__':
    app.run()
```



###### 使用Redis存储数据的chain: <demo>

```python
from apiserver import app
from chain import Memory,Redis

app = app
app.chain = Redis(host='127.0.0.1')


if __name__ == '__main__':
    app.run()
```



可选参数:

```yaml
Memory:
  lasting=False				# 数据是否持久化 默认 False	
  filename='Chain.json'		# 持久化保存路径 默认 'Chain.json'
  
Redis:
  host='127.0.0.1', 		# redis服务器ip 默认 127.0.0.1
  port=6379, 				# 端口号 默认 6379
  decode_responses=True, 	# 保持默认就好
  lasting=True, 			# 数据是否持久化 默认 True	
  keys='queue'				# 列表在数据库中的key 默认 queue
```



#### 通过YAML配置文件使用Chain:

下载代码

导入到项目

安装依赖

编辑chain.yaml文件:

```yaml
# 内存模式
memorymode: false
memory:
  lasting: false    			  # 是否持久化
  filename: 'Chain.json'          # 持久化文件名

# redis模式
redismode: true
redis:
  host: 127.0.0.1   # redis服务器ip
  keys: queue       # 列表key
  lasting: true     # 是否持久化
  port: 6379        # 端口号

```

###### 注意: memorymode和redismode同时为true时,使用memorymode

通过app.py+uwsgi启动应用:

```
uwsgi --ini uwsgi.ini
```



#### 通过Docker使用Chain

下载代码

解压

##### 在项目目录内构建镜像:

```bash
docker build -f Dockerfile -t mek/chain:new .
```

##### 简单启动:

```bash
docker run -d -p 5000:5000 mek/chain:new
```

##### 使用自定义配置文件启动:

用户自己的chain.yaml替换容器内的/chain/chain.yaml文件.

```bash
docker run -d -p 5000:5000 -v ~/chain/chain.yaml:/chain/chain.yaml mek/chain:new
```

###### 或者修改chain.yaml 文件后重新构建镜像.



#### 使用提示

###### 少量数据+不需要持久化推荐使用 memory模式.

###### 少量数据+需要持久化推荐使用 memory模式.

###### 大量数据+不需要持久化推荐使用 memory模式.

###### 大量数据+需要持久化推荐使用 redis模式.

###### Docker或K8S集群部署一律使用redis模式.

因为memory持久化模式下,数据添加和取出都会有硬盘IO动作,当数据量过大时IO耗时将增大影响性能.



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
print(requests.post(url=host + 'clear', data={'passwd': '123456'}).json())

```



### 未来计划：

##### 编写将数据存储到Redis的模块：<已实现>

​	用于分布式部署api

##### Docker 支持:<已实现>

​	方便部署

##### 编写将数据存储到sqlite和mysql的模块:

​	方便嵌入到其他项目中

