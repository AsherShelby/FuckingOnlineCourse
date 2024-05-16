import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import MainWindow


class SettingForm(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # form variables
        self.minTime = ttk.StringVar(value="")
        self.maxTime = ttk.StringVar(value="")

        # form header
        hdr_txt = "输入刷视频时各种点击操作的间隔时间，"
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=5)
        hdr_txt = "程序会根据所给出的时间范围之内取一个随机值进行等待"
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=5)
        hdr_txt = "建议尽量提高最小等待时间，并扩大时间范围，减小被网站检测作弊的概率"
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=5)
        hdr_txt = ""
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=5)

        # form entries
        self.create_form_entry("最小等待时间",  self.minTime, MainWindow.minTime)
        self.create_form_entry("最大等待时间",  self.maxTime, MainWindow.maxTime)
        self.create_buttonbox()

    def create_form_entry(self, label, variable, nowValue):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=10)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)
        ent = ttk.Entry(master=container, textvariable=variable, width=10)
        ent.insert(0, str(nowValue))
        ent.pack(side=LEFT, padx=5, fill=X)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="保存",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="取消",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):
        if self.minTime.get().isdigit() and self.maxTime.get().isdigit():
            if int(self.minTime.get()) > int(self.maxTime.get()):
                Messagebox.ok("最小等待时间不能大于最大等待时间", "错误")
                return
            else:
                MainWindow.minTime = float(self.minTime.get())
                MainWindow.maxTime = float(self.maxTime.get())
                print(MainWindow.minTime, MainWindow.maxTime)
                self.on_cancel()
        else:
            Messagebox.ok("有非法输入", "错误")
            return

    def on_cancel(self):
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    app = ttk.Window("Data Entry", "superhero", resizable=(False, False))
    SettingForm(app)
    app.mainloop()

