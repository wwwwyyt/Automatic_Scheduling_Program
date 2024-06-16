import networkx as nx


class BipartiteGraph:
    def __init__(self, matrix: tuple, vertices_a: tuple, vertices_b: tuple):
        # 二部图中顶点集合的序号
        self.v_a = 0
        self.v_b = 1

        # 创建二部图的顶点编号与名称的关系
        self.a_name = {i: v for i, v in enumerate(vertices_a)}
        self.b_name = {i + len(self.a_name): v for i, v in enumerate(vertices_b)}

        # 创建二部图
        self.g = nx.Graph()
        self.g.add_nodes_from(range(len(vertices_a)), bipartite=self.v_a)
        self.g.add_nodes_from(range(len(vertices_b), len(vertices_b) + len(vertices_a)), bipartite=self.v_b)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == '是':
                    self.g.add_edge(i, j + len(vertices_a))
                elif matrix[i][j] == '否':
                    pass
                else:
                    print("数值错误：", matrix[i][j])

    def get_max_matching(self):
        matching_index = nx.maximal_matching(self.g)
        matching_name = []
        for edge in matching_index:
            a_index = edge[self.v_a]
            b_index = edge[self.v_b]
            matching_name.append((self.a_name[a_index], self.b_name[b_index]))
        return matching_index, matching_name

    def remove_edge(self, a_index: int, b_index: int):
        self.g.remove_edge(a_index, b_index)

    def remove_edges(self, edge_set: tuple):
        for edge in edge_set:
            a_index = edge[self.v_a]
            b_index = edge[self.v_b]
            self.g.remove_edge(a_index, b_index)

