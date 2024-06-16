import data2table as d2t


def create_is_workable_matrix(table_file: d2t.Table):
    col_start = 2
    col_end = table_file.col_count
    row_start = 1
    row_end = table_file.line_count

    is_workable = tuple(
        tuple(row[col_start:col_end] for row in
              table_file.table[row_start:row_end]
              )
    )
    return is_workable


def create_employee_weight_matrix(employees: tuple, on_duty_place: tuple):
    # 创建宿舍到值班地点的距离的表格
    dormitory = ("东", "西", "北", "新北")
    distance = {"东": {"东": 0, "西": 1, "北": 1},
                "西": {"东": 1, "西": 0, "北": 2},
                "北": {"东": 1, "西": 2, "北": 0},
                "新北": {"东": 2, "西": 3, "北": 1}}

    # 这是以宿舍为列，以人员为行的矩阵
    employee_weight = []
    for member in employees:
        row = []
        dormitory = member['dormitory']
        for place in on_duty_place:
            if dormitory not in distance:
                weight = 0
            else:
                weight = distance[dormitory][place]
            row.append(weight)
        employee_weight.append(tuple(row))
    return tuple(employee_weight)
