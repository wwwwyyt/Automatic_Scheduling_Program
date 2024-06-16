import networkx as nx
from scipy.optimize import linear_sum_assignment

import data2table as d2t
import vertex as v
import bipartite_graph as bg
import matrix as mat

# 读取格式化文件信息到二维元组中
table_file = d2t.Table()

# 创建顶点集合：人员信息、值班时间、值班地点
employees = v.create_employee_vertices_set(table_file)
on_duty_time = v.create_time_vertices_set(table_file)
on_duty_place = v.create_place_vertices_set()

# 创建二部图：可值班时间的二部图
is_workable = mat.create_is_workable_matrix(table_file)
employee_name = tuple(d['name'] for d in employees)
workable_time = bg.BipartiteGraph(is_workable, employee_name, on_duty_time)

group_on_each_time = {k: [] for k in on_duty_time}
group_member_num = 8
for i in range(group_member_num):
    matching_index, matching_name = workable_time.get_max_matching()
    workable_time.remove_edges(matching_index)  # 删除已安排的人员与值班时间组合
    for u in matching_name:
        time = u[workable_time.v_b]
        name = u[workable_time.v_a]
        group_on_each_time[u[workable_time.v_b]].append(u[workable_time.v_a])

# 打印每个人的值班次数
with open('值班安排结果.txt', 'w') as outfile:
    # 打印值班安排
    for time in group_on_each_time:
        # 向文件输出
        outfile.write(time + '\t')
        for member in group_on_each_time[time]:
            outfile.write(member + '\t')
        outfile.write('\n')
        # 向控制台输出
        print(time, group_on_each_time[time])
