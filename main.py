import networkx as nx

with open('data.txt', 'r', encoding='utf-8') as infile:
    infile_lines = infile.readlines()

line_count = len(infile_lines)
col_count = len(infile_lines[0].split())


# 检测每一行的单词数是否相同
def check_format(standard_col_count: int, file_lines):
    is_first_line = True
    for row in file_lines:
        if is_first_line:
            words = row.split()
            standard_col_count = len(words)
            is_first_line = False
        else:
            words = row.split()
            if len(words) != standard_col_count:
                raise ValueError("表格文件格式错误")


# 检查文件格式并将读取内容按空白字符分割，最终输出表格table
table = []
try:
    check_format(col_count, infile_lines)
    for line in infile_lines:
        table.append(line.split())
    table = tuple(table)
except ValueError as e:
    print(ValueError)

# 创建人员集合
employee = []
for i in range(1, len(table)):
    employee.append(table[i][0])
employee = tuple(employee)

# 创建值班安排集合
on_duty_schedule = []
on_duty_time = []
on_duty_place = ('东', '西', '北')
for i in range(2, col_count):
    on_duty_time.append(table[0][i])
for time in on_duty_time:
    for place in on_duty_place:
        on_duty_schedule.append((time, place))
on_duty_schedule = tuple(on_duty_schedule)

# 创建人员与其被安排的值班次数的表格（保证每个人不会连续两天都参与上午的值班）
on_duty_count = {}
for i in range(len(employee)):
    on_duty_count[employee[i]] = 0
on_duty_in_the_morning_count = {}
for i in range(len(employee)):
    on_duty_in_the_morning_count[employee[i]] = 0

# 创建二部图的顶点编号与名称的关系。employee集合与on_duty_time集合是两个顶点集合。
employee_table = {}
for i in range(len(employee)):
    employee_table[i] = employee[i]
on_duty_time_table = {}
for i in range(len(employee), len(on_duty_time) + len(employee)):
    on_duty_time_table[i] = on_duty_time[i - len(employee)]

# 创建二部图：可值班时间的二部图
EMPLOYEE = 0  # 二部图中employee顶点集合的序号
ON_DUTY_TIME = 1  # 二部图中on_duty_time顶点集合的序号
is_workable = nx.Graph()
is_workable.add_nodes_from(range(len(employee)), bipartite=EMPLOYEE)
is_workable.add_nodes_from(range(len(employee), len(on_duty_time) + len(employee)), bipartite=ON_DUTY_TIME)
for i in range(1, line_count):
    for j in range(2, col_count):
        if table[i][j] == '是':
            is_workable.add_edge(i - 1, j - 2 + len(employee))
        elif table[i][j] == '否':
            pass
        else:
            print("数值错误：", table[i][j])

# 创建值班安排表格
schedule_table = {}
for duty_time in on_duty_time:
    schedule_table[duty_time] = []

# 进行求“最大匹配 - 删除最大匹配 - 再次求最大匹配”的迭代
# 需要几组人员就进行几次迭代
GROUP_NUM = 10  # 默认有每个时间段需要两组人员
for i in range(GROUP_NUM):
    # 求二部图的最大匹配
    matching = nx.maximal_matching(is_workable)

    # 将二部图的最大匹配加入值班安排表格
    for edge in matching:

        # 获取一种值班组合（时间 - 人员）
        a = edge[ON_DUTY_TIME]
        b = edge[EMPLOYEE]
        time = on_duty_time_table[a]
        member = employee_table[b]

        # 当值班次数已经达到2或者已经在上午值班，不要添加该值班组合
        if on_duty_count[member] == 2 or on_duty_in_the_morning_count[member] == 1:
            continue

        # 将该值班组合加入值班安排表格
        schedule_table[time].append(member)

        # 计数每个员工的总值班次数和在上午值班的次数
        on_duty_count[member] += 1
        if '上午' in time:
            on_duty_in_the_morning_count[member] += 1

        is_workable.remove_edge(a, b)  # 删除已安排的人员与值班时间组合

# 打印每个人的值班次数
with open('值班安排结果.txt', 'w') as outfile:
    # 打印值班安排
    for time in schedule_table:
        outfile.write(time + '\t')
        for member in schedule_table[time]:
            outfile.write(member + '\t')
        outfile.write('\n')
        print(time, schedule_table[time])

    for member in on_duty_count:
        print(member, "值了", on_duty_count[member], "次班")
        if on_duty_in_the_morning_count[member] >= 2:
            print(member, "在上午值班的次数过多")
