# coding=utf-8
import operator
from resource import Resource
from task import Task
# Task.random_queues(int(input("请输入任务数：")))


class Algorithm:    # 类后没有()
    """调度算法类"""
    ri1 = 0     # 初始化任务所需资源
    ri2 = 0
    ri3 = 0

    def __init__(self):     # 两个参数
        """初始化属性"""

    @classmethod
    def get_pi_resource(cls, pi):
        """获取任务所需的系统资源"""
        i = Task.find_pi(Task.waiting_queues, pi)[1]
        Algorithm.ri1 = Task.waiting_queues[i][1]  # 获取任务所需的系统cpu资源
        Algorithm.ri2 = Task.waiting_queues[i][2]
        Algorithm.ri3 = Task.waiting_queues[i][3]

    @classmethod
    def judge(cls, t, ti):  # 到达时间t，系统时间ti
        """时间和资源判断"""
        r_cpu = Resource.get_res()[0]
        r_mem = Resource.get_res()[1]
        r_io = Resource.get_res()[2]
        if t <= ti and Algorithm.ri1 <= r_cpu and Algorithm.ri2 <= r_mem and Algorithm.ri3 <= r_io:
            return True

    @classmethod
    def response_ratio(cls, ti):
        """计算ti时刻等待任务的响应比"""
        # 计算响应比 1 + w/T
        new_waiting_queues = Task.waiting_queues.copy()
        for i in range(len(new_waiting_queues)):  # 遍历队列
            pi = new_waiting_queues[i][0]
            j = Task.find_pi(new_waiting_queues, pi)[1]
            t = new_waiting_queues[j][4]

            if t <= ti:
                w = ti - Task.waiting_queues[j][4]
                T = Task.waiting_queues[j][5]
                s = 1 + w / T
                Task.waiting_queues[j][7] = round(s, 2)  # 保留两位小数

    @classmethod
    def scheduling(cls, pi, t, ti):     # 任务pi,到达时间t，系统时间ti
        """调度单个任务"""
        # 获取任务所需的系统资源
        Algorithm.get_pi_resource(pi)

        # 计算每个任务的响应比
        # Algorithm.response_ratio(pi, t, ti)

        if Algorithm.judge(t, ti):
            # 分配系统资源给任务pi
            Resource.allocate_res(Algorithm.ri1, Algorithm.ri2, Algorithm.ri3)

            # 将任务pi加入到运行队列
            i = Task.find_pi(Task.waiting_queues, pi)[1]
            print("Scheduling task: ", Task.waiting_queues[i])
            Task.add_running_pi(pi, ti)

            # 将任务pi从等待队列中剔除
            Task.del_waiting_pi(pi)

    @classmethod
    def fifo(cls):
        """先来先服务调度"""
        print("FIFO")
        Task.waiting_queues.sort(key=operator.itemgetter(4))  # FIFO  到达时间非递减排序

    @classmethod
    def sjf(cls):
        """短作业优先调度"""
        print("SJF")
        Task.waiting_queues.sort(key=operator.itemgetter(5))  # SJF  运行时间非递减排序

    @classmethod
    def psa(cls):
        """优先级调度"""
        print("PSA")
        Task.waiting_queues.sort(key=operator.itemgetter(6), reverse=True)  # PSA 优先级非递增排序
        return

    @classmethod
    def hrrf(cls):
        """高响应比优先调度"""
        print("HRRF")
        Task.waiting_queues.sort(key=operator.itemgetter(4, 5))  # 先按到达时间非递减排序，再按运行时间非递减排序
        Task.waiting_queues.sort(key=operator.itemgetter(7), reverse=True)  # HRRF 最终排序：响应比非递增排序



