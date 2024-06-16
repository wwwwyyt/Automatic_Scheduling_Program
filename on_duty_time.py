import data2table as d2t


def create_time_vertices_set(table_file: d2t.Table):
    on_duty_time = []
    for i in range(2, table_file.col_count):
        on_duty_time.append(table_file[0][i])
    on_duty_time = tuple(on_duty_time)
