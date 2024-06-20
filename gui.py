import tkinter as tk
import main


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("收书活动排班程序")
        self.root.geometry("320x320")
        self.entry_label = tk.Label(self.root, text="粘贴表格内容")
        self.entry_label.pack(side=tk.TOP)
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack()
        self.run_button = tk.Button(self.root, text="运行程序", command=self.on_run_button_clicked)
        self.run_button.pack()
        self.output_label = tk.Label(self.root, text="排班结果输出")
        self.output_label.pack()
        self.output_text = tk.Text(self.root, height=16, width=40)
        self.output_text.pack()

    def run(self):
        self.root.mainloop()

    def write_to_text(self, message):
        self.output_text.insert(tk.END, message)

    def on_run_button_clicked(self):
        user_input = self.entry.get()
        with open("data.txt", "w", encoding='utf-8') as outfile:
            outfile.write(user_input)
        res = main.main()
        self.write_to_output_text(res)

    def write_to_output_text(self, group_on_each_place_on_each_time):
        for time in group_on_each_place_on_each_time:
            self.write_to_text(time + '\n')
            for place in group_on_each_place_on_each_time[time][0]:
                self.write_to_text(place + ' ')
                for members in group_on_each_place_on_each_time[time][0][place]:
                    self.write_to_text(members + ' ')
                self.write_to_text('\n')


# 创建程序窗口
window = GUI()
window.run()
