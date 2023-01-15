import os
import yaml
from apiserver import app
from chain import Redis, Memory


def load_config():  # 加载配置文件

    with open('chain.yaml', 'r') as f:
        return yaml.safe_load(f)


def createengine(dic=load_config()):
    """构建实例化对象"""
    if os.path.exists('chain.yaml'):  # 判断配置文件是否存在
        if dic.get('memorymode'):
            lasting = dic.get('memory').get('lasting')
            filename = dic.get('memory').get('filename')
            return Memory(lasting=lasting, filename=filename)

        elif dic.get('redismode'):
            host = dic.get('redis').get('host')
            port = dic.get('redis').get('port')
            keys = dic.get('redis').get('keys')
            lasting = dic.get('redis').get('lasting')

            return Redis(host=host, port=port, keys=keys, lasting=lasting)


        else:
            return Memory()
    else:
        return Memory()


app = app

app.chain = createengine()

if __name__ == '__main__':
    print(app.chain.version)
