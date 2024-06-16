import data2table as d2t


def create_employee_vertices_set(table_file: d2t.Table):
    employees = []
    for i in range(1, len(table_file.table)):
        employee = {'name': table_file.table[i][0],
                    'dormitory': table_file.table[i][1]}
        employees.append(employee)
    return employees
