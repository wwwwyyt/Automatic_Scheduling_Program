import data2table as d2t


def create_employee_vertices_set(table_file: d2t.Table):
    employees = []
    for i in range(1, len(table_file.table)):
        employee = {'name': table_file.table[i][0],
                    'dormitory': table_file.table[i][1],
                    'on_duty_count': 0,
                    'on_duty_in_the_morning_count': 0}
        employees.append(employee)
    return employees


def create_time_vertices_set(table_file: d2t.Table):
    on_duty_time = tuple(time for time in table_file.table[0][2:])
    return on_duty_time


def create_place_vertices_set():
    on_duty_place = ('东', '西', '北')
    return on_duty_place
