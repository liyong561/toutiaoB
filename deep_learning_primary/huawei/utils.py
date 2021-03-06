'''
车辆直行通过cross时的s（位置）,车辆的位置很重要。
v1:道路1的限速，v2:道路2的限速，v:车辆的限速.u：车辆的实际速度。

在调度时，汽车有两个状态，调度开始和调度终止状态。

还要设计一个向量表示车辆在t时刻的状态：
这是原始的车辆信息：(车辆id，始发地、目的地、最高速度、计划出发时间)
新的向量主要作用，车辆在哪个路断了，前方是否有车辆等，字段可以冗余
(车辆id，始发地、目的地、最高速度、计划出发时间，时刻t，道路id，起点，终点，相对于起点位置s，道路限速，)
但是以车辆为单位来调度，显然次数太多，还是要以道路id（为单位）来调度
 (道路id，道路长度，最高限速，车道数目，起始点id，终点id，是否双向)
 [car_id,s,channel，direction]，构造这个数据块，非常的重要。
'''

import math


def read_table(file):
    data = {}
    # i = 0;第一个字段为key，使用dict,很方便访问
    with open(file) as f:
        for line in f:  # 直接是line
            record = line.strip()
            if record.startswith('#'):  # 跳过注释。
                continue
            '''
            eval()这个函数非常的神奇，读取这种数据，简直不要太方便
            把字符串变成了元组，而元组和列表的转换非常方便。但是元组的修改不如列表方便。（12，，，12，，）
            '''
            ls = list(eval(record))
            # print(ls)
            data[ls[0]] = ls  # add item to the dictionary,去掉制表符，换行符。
            # i+=1 # don't have the i++
    # print(len(data))  # 获取数据的整体信息也非常方便
    # print(data)
    return data


def init_status(road_with_car):
    for road_with_car_value in road_with_car.values():
        for record in road_with_car_value:
            record[4] = 0  # 重新变为等待调度状态。改变了传入的参数。


def rotate_list(ls, idx):
    length = len(ls)
    ls1 = ls.copy()
    ls1[0:length - idx] = ls[idx:length]
    ls1[length - idx:length] = ls[0:idx]
    return ls1


# 返回0，1，2，3的顺序，这个方法有问题。
def number_position(theta_rel):
    sin = int(math.sin(theta_rel))
    cos = int(math.cos(theta_rel))
    if cos == 0:
        if sin == 1:
            return 1
        else:
            return 3
    else:
        if cos == 1:
            return 0
        else:
            return 2


def new_number_position(number, x, y, l):
    if number == 0:
        return [x + l, y]
    if number == 1:
        return [x, y + l]
    if number == 2:
        return [x - l, y]
    if number == 3:
        return [x, y - l]


def get_road_id(ls, ls1):
    for x in ls:
        if x != -1:
            for y in ls1:
                if x == y:
                    return x


def dictionary_file(dict1):
    f = open('answer.txt', mode='w')
    for key in dict1:
        dict1[key].insert(0, key)
        f.write(str(tuple(dict1[key])))  # 只能写str？
        f.write('\n')
