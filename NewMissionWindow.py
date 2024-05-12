import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


def has_chinese_char(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))


class DataEntryForm(ttk.Frame):
    mission_infor_dic = {}
    master = None

    def __init__(self, master, mission_infor_dic):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.mission_infor_dic = mission_infor_dic
        self.master = master
        # form variables
        self.name = ttk.StringVar()
        self.id = ttk.StringVar()
        self.password = ttk.StringVar()
        self.school = ttk.StringVar()
        self.platform = ttk.StringVar()

        school_lst = ['中南林业科技大学涉外学院', '北京嘉华大学工商学院']
        platform_lst = ['英华学堂', '仓辉教育科技']

        # form header
        hdr_txt = "请输入任务信息："
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("任务名称", self.name)
        self.create_form_combox("学校：", self.school, school_lst)
        self.create_form_combox("平台：", self.platform, platform_lst)
        self.create_form_entry("学号：", self.id)
        self.create_form_entry("密码：", self.password)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        lbl = ttk.Label(master=container, text=label.title(), width=10)
        ent = ttk.Entry(master=container, textvariable=variable)

        lbl.pack(side=LEFT, padx=5)
        container.pack(fill=X, expand=YES, pady=5)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_form_combox(self, label, variable, lst):
        container = ttk.Frame(self)
        lbl = ttk.Label(master=container, text=label.title(), width=10)
        # ddl = ttk.Entry(master=container, textvariable=variable)
        ddl = ttk.Combobox(master=container, textvariable=variable)
        ddl['value'] = lst
        ddl['state'] = 'readonly'
        ddl.current(0)
        lbl.pack(side=LEFT, padx=5)
        container.pack(fill=X, expand=YES, pady=3)
        ddl.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="确定",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        # cnl_btn = ttk.Button(
        #     master=container,
        #     text="取消",
        #     command=self.on_cancel,
        #     bootstyle=DANGER,
        #     width=6,
        # )
        # cnl_btn.pack(side=RIGHT, padx=10)

    def on_submit(self):
        """Print the contents to console and return the values."""
        # print("任务名称:", self.name.get())
        # print("学校:", self.school.get())
        # print("学号:", self.id.get())
        # print("密码:", self.password.get())

        self.mission_infor_dic['name'] = self.name.get()
        self.mission_infor_dic['school'] = self.school.get()
        self.mission_infor_dic['id'] = self.id.get()
        self.mission_infor_dic['password'] = self.password.get()
        self.mission_infor_dic['platform'] = self.platform.get()

        for key, value in self.mission_infor_dic.items():
            if value == '':
                Messagebox.ok(message='你是不是还有一些东西没输入（敲脑袋）')
                return
            if key == 'id' and has_chinese_char(value):
                Messagebox.ok(message='我活这么久第一次见中文学号')
                return
            if key == 'password' and has_chinese_char(value):
                Messagebox.ok(message='我活这么久还是第一次见密码里有中文')
                return

        if self.platform.get() == '仓辉教育科技':
            self.mission_infor_dic['school'] += '实训平台'

        self.master.quit()
        self.master.destroy()
    # def on_cancel(self):
    #     """Cancel and close the application."""
    #     self.destroy()

