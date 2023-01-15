import os
import yaml

if os.path.exists('chain.yaml'):
    pass

else:
    pass

'''恢复默认的yaml配置文件'''


def yamlll():
    dic = {
        # 内存模式
        'memorymode': True,
        'memory': {'lasting': False, 'filename': 'Chain.json'},

        # redis模式
        'redismode': False,
        'redis': {'host': '127.0.0.1', 'port': 6379, 'keys': 'queue', 'lasting': True}

    }
    with open('chain.yaml', 'w') as f:
        yaml.safe_dump(dic, f)


if __name__ == '__main__':
    yamlll()
