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
