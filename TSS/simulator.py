# coding=utf-8
import operator
import matplotlib.pyplot as plt
from algorithm import Algorithm     # 导入算法模块
from task import Task
from resource import Resource

news_waiting_queues = Task.waiting_queues_copy


def print_ti(ti):
    """打印系统时间"""
    if ti == 1:
        print("First second:")
    elif ti == 2:
        print("Second second:")
    elif ti == 3:
        print("The third second:")
    else:
        print("The " + str(ti) + "th second:")


def release_task_res(pi):
    """查找任务pi,并释放其分配的系统资源"""
    for i in range(len(news_waiting_queues)):
        if news_waiting_queues[i][0] == pi:
            r_cpu = news_waiting_queues[i][1]  # 查看原始信息
            r_mem = news_waiting_queues[i][2]
            r_io = news_waiting_queues[i][3]

            Resource.release_res(r_cpu, r_mem, r_io)  # 释放资源

            break


def task_complete(ti):
    """判断是否有任务完成"""
    new_running_queues = Task.running_queues.copy()
    for pi in new_running_queues.keys():
        if Task.is_complete(pi, ti):
            t1 = new_running_queues[pi]     # 完成时刻
            i = Task.find_pi(news_waiting_queues, pi)[1]
            t = news_waiting_queues[i][4]       # 到达时刻

            Task.complete_time.append(t1 - t)   # 加入任务完成时间列表
            # print(Task.complete_time)

            average_complete_time = round(sum(Task.complete_time)/len(Task.complete_time), 2)   # 计算平均完成时间
            Task.average_complete_time.append(average_complete_time)    # 加入列表
            # print("Average complete time is: ", average_complete_time)

            print("Task " + str(pi) + " running completed，complete time C" + str(i + 1) + " is " + str(t1 - t) + " s.")
            Task.del_running_pi(pi)  # 剔除任务

            release_task_res(pi)    # 释放资源


def scheduling_pi(ti):
    """调度任务，可调度多个任务"""
    # 对每个任务计算响应比
    Algorithm.response_ratio(ti)

    # 对任务队列排序,高响应比优先
    Algorithm.hrrf()
    Task.print_queue()

    # 调度任务
    new_waiting_queues = Task.waiting_queues.copy()
    for i in range(len(new_waiting_queues)):  # 遍历队列
        pi = new_waiting_queues[i][0]
        j = Task.find_pi(new_waiting_queues, pi)[1]
        t = new_waiting_queues[j][4]

        Algorithm.scheduling(pi, t, ti)  # 调度单个任务


def print_task_numbers():
    """打印队列剩余任务数量"""
    if Task.len_running() in [0, 1]:
        print("The running queues have " + str(Task.len_running()) + " task.")
    else:
        print("The running queues have " + str(Task.len_running()) + " tasks.")

    if Task.len_waiting() in [0, 1]:
        print("The waiting queues have " + str(Task.len_waiting()) + " task.\n")
    else:
        print("The waiting queues have " + str(Task.len_waiting()) + " tasks.\n")


def drawing(name):
    """绘制折线图"""
    input_values = [i for i in range(1, len(Task.average_complete_time) + 1)]   # 任务数量
    # 提供输入输出，改变x轴第一个输出，"x-":节点标识
    plt.plot(input_values, Task.average_complete_time, "*-", label="Average Complete Time")
    plt.plot(input_values, Task.complete_time, "x-", label="Task Complete Time")
    plt.title(name + ": Average Complete Time")
    plt.xlabel("Numbers of Task")
    plt.ylabel("Average Complete Time(s);Task Complete Time(s)")

    plt.grid(True)         # 显示网格
    plt.legend()           # 显示图例
    plt.show()


def execute(a_name):
    """模拟执行任务"""
    try:
        ti = 1
        while True:
            # 打印系统时间
            print_ti(ti)

            # 判断是否有任务完成
            task_complete(ti)

            if Task.len_waiting() > 0:
                # 调度任务
                scheduling_pi(ti)

            elif Task.len_running() == 0:
                print("The queues of running and waiting is empty, the end.")
                name = a_name
                drawing(name)   # 绘制折线图
                break
            # 打印队列剩余任务数量
            print_task_numbers()
            ti += 1
    except RuntimeError:
        print("Error！")


# FIFO
# Algorithm.fifo()

# SJF
# Algorithm.sjf()

# PSA
# Algorithm.psa()

# HRRF
Algorithm.hrrf()

Task.print_queue()  # 打印任务队列
name = 'HRRF'
execute(name)





