# 定义Table类
class Table:
    # 初始化方法，默认从data.txt初始化
    def __init__(self, infile_name='data.txt'):
        with open(infile_name, 'r', encoding='utf-8') as infile:
            self.infile_lines = infile.readlines()

        self.line_count = len(self.infile_lines)
        self.col_count = len(self.infile_lines[0].split())

        # 检查文件格式并将读取内容按空白字符分割，最终输出表格table
        self.table = []
        try:
            self.__check_format()
            for line in self.infile_lines:
                self.table.append(line.split())
            self.table = tuple(self.table)
        except ValueError as e:
            print(e)
            x = input('程序错误终止，按任意键退出...')

    # 检查格式
    def __check_format(self):
        standard_col_count = self.col_count
        if standard_col_count <= 2:
            raise ValueError("表格文件列数过少")
        is_first_line = True
        for row in self.infile_lines:
            if is_first_line:
                words = row.split()
                standard_col_count = len(words)
                is_first_line = False
            else:
                words = row.split()
                if len(words) != standard_col_count:
                    raise ValueError("表格文件格式错误")
