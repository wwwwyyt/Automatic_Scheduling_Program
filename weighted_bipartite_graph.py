import numpy as np
from scipy.optimize import linear_sum_assignment


class WeightedBipartiteGraph:
    def __init__(self, vertices_row: tuple, vertices_col: tuple, weight_matrix: tuple):
        self.row_name = vertices_row
        self.col_name = vertices_col
        self.row_cnt = len(vertices_row)
        self.col_cnt = len(vertices_col)
        self.v_row = 0
        self.v_col = 1
        self.cost_matrix = np.array(weight_matrix)

    def get_minimum_weight_matching(self):
        row_index, col_index = linear_sum_assignment(self.cost_matrix)
        matching_index = tuple(zip(row_index, col_index))
        matching_name = []
        for e in matching_index:
            edge = (self.row_name[e[self.v_row]], self.col_name[e[self.v_col]])
            matching_name.append(edge)
        return matching_index, tuple(matching_name)

    def remove_edges(self, edge_set: tuple):
        for edge in edge_set:
            self.cost_matrix[edge[self.v_row]][edge[self.v_col]] = 99

    def display(self):
        print('列\\行 ', end='')
        for c in self.col_name:
            print(c, end=' ')
        print(end='\n')
        for i in range(self.row_cnt - 1):
            print(self.row_name[i], end=' ')
            for j in range(self.col_cnt):
                print(self.cost_matrix[i][j], end=' ')
            print(end='\n')
