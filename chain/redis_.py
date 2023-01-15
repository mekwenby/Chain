import redis


class Chain:
    def __init__(self, host='127.0.0.1', port=6379, decode_responses=True, lasting=True, keys='queue'):
        """
        host = 主机IP
        port = 端口号
        keys = 队列在数据库中的key
        """

        '''持久化标记'''
        self.lasting = lasting
        '''创建链接'''
        self.redis = redis.Redis(host=host, port=port, decode_responses=decode_responses)
        self.version = 'redis_s1.1_8'
        '''列表的key'''
        self.queue = keys
        self.index = -1
        self.passwd = '123456'
        '''不持久化时清空列表'''
        if not self.lasting:
            self.clear()

    def lastinger(self):  # 持久化
        self.redis.save()

    def add(self, data):
        """添加"""
        self.redis.rpush(self.queue, data)
        return self.redis.llen(self.queue)

    def adds(self, datas):
        """添加多个"""
        for i in datas:
            self.redis.rpush(self.queue, i)
        return self.redis.llen(self.queue)

    def get(self):
        """获取"""
        if self.index == -1:
            return self.redis.rpop(self.queue)
        else:
            return self.redis.lpop(self.queue)

    def len(self):
        """获得长度"""
        return self.redis.llen(self.queue)

    def delete(self, data):
        """删除"""
        n = self.len()
        self.redis.lrem(self.queue, value=data, count=1)
        return n - self.len()

    def deletes(self, datas):
        """删除多个"""
        n = self.len()
        for i in datas:
            self.redis.lrem(self.queue, 1, i)
        return n - self.len()

    def printall(self):
        """打印全部"""
        for i in self.redis.lrange(self.queue, 0, -1):
            print(i)

    def clear(self):  # 清空队列，返回清空数量
        """清空列表"""
        n = self.len()
        self.redis.delete(self.queue)
        self.lastinger()
        return n
