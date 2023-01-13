import json
from threading import Thread


class Chain:
    def __init__(self, lasting=False):
        self.lasting = lasting  # 是否持久化
        self.file = 'Chain.json'  # 持久化文件路径
        self.queue = list()
        self.version = 'memory_1.0'
        self.passwd = '123456'  # 密码 用于api清空队列

        '''如果需要持久化，从文件加载数据'''
        if self.lasting:
            self.load()

    def lastinger(self):  # 持久化
        if self.lasting:
            with open(self.file, 'w', encoding='utf-8') as file:
                '''将保存动作添加到其他线程'''
                Thread(target=json.dump, args=(self.queue, file)).run()

    def load(self):  # 从文件加载
        with open(self.file, 'r', encoding='utf-8') as file:
            self.queue = json.load(file)

    def add(self, s):  # 添加
        self.queue.append(s)
        self.lastinger()

    def adds(self, lis):  # 批量添加 传入可迭代对象
        for i in lis:
            self.queue.append(i)
        self.lastinger()

    def get(self):  # 获取
        if len(self.queue) > 0:
            c = self.queue.pop()
            self.lastinger()
            return c
        else:
            return None

    def printall(self):  # 打印全部
        for i in self.queue:
            print(i)

    def clear(self):  # 清空队列，返回清空数量
        lens = len(self.queue)
        self.queue = list()
        self.lastinger()
        return lens

    def len(self):
        return len(self.queue)
