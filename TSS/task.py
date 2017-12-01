# coding=utf-8
import random


class Task:
    """任务类"""
    waiting_queues = [
        # Pi：任务名,r1：CPU资源需求,r2：MEM资源需求,r3：IO资源需求,t：到达时间,T：任务完成时间,p：优先级
        ['P1', 0.3, 0.1, 0.2, 1, 2, 1, 1],
        ['P2', 0.2, 0.5, 0.5, 2, 4, 1, 1],
        ['P3', 0.4, 0.2, 0.5, 4, 1, 2, 1],
        ['P4', 0.5, 0.3, 0.3, 3, 2, 1, 1],
        ['P5', 0.4, 0.4, 0.3, 2, 3, 2, 1],
        ['P6', 0.4, 0.3, 0.1, 5, 3, 1, 1],
        ['P7', 0.3, 0.4, 0.3, 5, 2, 3, 1],
        ['P8', 0.2, 0.5, 0.3, 3, 1, 3, 1],
    ]
    # 类变量
    waiting_queues_copy = waiting_queues.copy()        # 释放任务资源时用
    # waiting_queues = []
    # waiting_queues_copy = []  # 释放任务资源时用
    running_queues = {}
    complete_time = []          # 任务的完成时间
    average_complete_time = []  # 任务的平均完成时间

    def __init__(self):
        """初始化属性"""

    @classmethod            # 类方法
    def random_queues(cls, n):  # cls 类方法的第一个参数，类似成员方法中的self
        """随机产生n个任务"""
        for i in range(0, n):
            pi = "P" + str(i + 1)
            r1 = random.randint(1, 5) / 10       # CPU资源需求：0.1-0.5
            r2 = random.randint(1, 5) / 10
            r3 = random.randint(1, 5) / 10
            t = random.randint(1, 5)             # 到达时刻: 1-5s
            T = random.randint(1, 5)             # 运行时间: 1-5s

            Task.waiting_queues.append([pi, r1, r2, r3, t, T])

        Task.waiting_queues_copy = Task.waiting_queues.copy()
        return Task.waiting_queues

    @classmethod
    def add_running_pi(cls, pi, ti):    # 任务pi、系统时间ti
        """添加任务到运行队列"""
        p_i = Task.find_pi(Task.waiting_queues, pi)[0]
        i = Task.find_pi(Task.waiting_queues, pi)[1]
        Task.running_queues[p_i] = ti + Task.waiting_queues[i][5]       # 任务的完成时间

    @classmethod
    def find_pi(cls, queues, pi):
        """找到任务队列中pi,返回任务pi和pi的所在位置索引i"""
        for i in range(len(queues)):
            if queues[i][0] == pi:
                return pi, i

    @classmethod
    def del_waiting_pi(cls, pi):
        """从等待队列中剔除任务"""
        i = Task.find_pi(Task.waiting_queues, pi)[1]
        del Task.waiting_queues[i]

    @classmethod
    def del_running_pi(cls, pi):
        """从运行队列中剔除任务"""
        del Task.running_queues[pi]

    @classmethod
    def time_complete(cls, pi):
        """输出任务的完成时间"""
        return Task.running_queues[pi]

    @classmethod
    def len_waiting(cls):
        """输出等待队列中任务个数"""
        return len(Task.waiting_queues)

    @classmethod
    def len_running(cls):
        """输出运行队列中任务个数"""
        return len(Task.running_queues)

    @classmethod
    def is_complete(cls, pi, ti):  # 任务pi,系统时间ti
        """判断运行队列中是否有任务完成"""
        if Task.running_queues[pi] == ti:
            return True
        else:
            return False

    @classmethod
    def print_queue(cls):
        """打印任务队列"""
        print("task queues：")
        for pi in range(len(Task.waiting_queues)):
            print(Task.waiting_queues[pi][0], ":", Task.waiting_queues[pi][1:8])
        print("\n")


"""
task = Task()
task.random_queues(10
                   )
task.print_queue()

print(task.waiting_queues)

#task.print_queue()
#print(task.waiting_queues_copy)

task.add_running_pi('P3', 5)
print(task.running_queues)

task.del_waiting_pi('P3')
print(task.waiting_queues)

#task.del_running_pi('P3')
#print(task.running_queues)
"""







