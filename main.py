import data2table as d2t
import vertex as v
import bipartite_graph as bg
import weighted_bipartite_graph as wbg
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
# 计算二部图最大匹配
group_on_each_time = {k: [] for k in on_duty_time}
group_member_num = 8
for i in range(group_member_num):
    matching_index, matching_name = workable_time.get_max_matching()
    workable_time.remove_edges(matching_index)  # 删除已安排的人员与值班时间组合
    for u in matching_name:
        time = u[workable_time.v_b]
        name = u[workable_time.v_a]
        group_on_each_time[u[workable_time.v_b]].append(u[workable_time.v_a])

'''
# 打印排班结果
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
'''

# 对于每个值班时间，创建带权二部图（每个成员到每个值班地点的值班成本）
group_on_each_place_on_each_time = {k: [] for k in on_duty_time}
for each_time in group_on_each_time:
    group_on_each_place = {k: [] for k in on_duty_place}
    member_names = group_on_each_time[each_time]
    members = []
    for name in member_names:
        member = [d for d in employees if d.get('name') == name]
        members.append(member[0])
    employee_weight_matrix = mat.create_employee_weight_matrix(tuple(members), on_duty_place)  # 生成该小组中每个成员值班的成本
    # print(employee_weight_matrix)

    # 计算二部图最小权匹配
    employee_weight = wbg.WeightedBipartiteGraph(tuple(member_names), on_duty_place, employee_weight_matrix)
    group_member_num = 3
    for i in range(group_member_num):
        matching_index, matching_name = employee_weight.get_minimum_weight_matching()

        edges_to_remove = tuple((x[employee_weight.v_row], y) for x in matching_index for y in range(employee_weight.col_cnt))
        employee_weight.remove_edges(edges_to_remove)  # 删除已安排的人员与值班地点组合
        for u in matching_name:
            group_on_each_place[u[employee_weight.v_col]].append(u[employee_weight.v_row])
    group_on_each_place_on_each_time[each_time].append(group_on_each_place)

# 向控制台输出
for time in group_on_each_place_on_each_time:
    print(time)
    for place in group_on_each_place_on_each_time[time][0]:
        print(place, end=' ')
        for members in group_on_each_place_on_each_time[time][0][place]:
            print(members, end=' ')
        print(end='\n')

# 向文件输出
with open('值班安排结果.txt', 'w') as outfile:
    for time in group_on_each_place_on_each_time:
        outfile.write(time + '\n')
        for place in group_on_each_place_on_each_time[time][0]:
            outfile.write(place + ' ')
            for members in group_on_each_place_on_each_time[time][0][place]:
                outfile.write(members + ' ')
            outfile.write('\n')
