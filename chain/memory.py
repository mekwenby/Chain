import json
import os
from threading import Thread


class Redis:
    def __init__(self, lasting=False, filename='Chain.json'):
        self.lasting = lasting  # 是否持久化
        self.file = filename  # 持久化文件路径
        self.queue = list()
        self.version = 'memory_1.3-qrv'
        self.passwd = '123456'  # 密码 用于api清空队列
        self.index = -1  # 索引 设置为 -1 先进后出,设置为 0 先进先出
        '''如果需要持久化，从文件加载数据'''
        if self.lasting:
            if os.path.exists(self.file):
                self.load()
            else:
                pass

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

    def delete(self, *args):  # 删除
        """传入任意数量的参数,返回删除的个数"""
        now = len(self.queue)
        for i in args:
            try:
                self.queue.remove(i)
            except:
                print(i, ' not in queue!')
        return now - len(self.queue)

    def deletes(self, lis):  # 批量删除
        """传入可迭代对象,返回删除的个数"""
        now = len(self.queue)
        for i in lis:
            try:
                self.queue.remove(i)
            except:
                print(i, ' not in queue!')
        return now - len(self.queue)

    def get(self):  # 获取
        if len(self.queue) > 0:
            c = self.queue.pop(self.index)
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
