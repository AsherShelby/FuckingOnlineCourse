import ctypes
import queue
import threading
import tkinter
from datetime import datetime
import ttkbootstrap as ttk
from selenium.common import NoSuchWindowException
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText

import FuckOnlineCourse
import frozen_dir
from NewMissionWindow import DataEntryForm

PATH = frozen_dir.app_path()


class MainFrame(ttk.Frame):
    tv = None
    mission_list = []
    curr_choose_index = 0
    mission_begin_btn = None
    mission_stop_btn = None
    threading_list = []
    scroll_text_list = []
    output_container = None
    after_scroll_text = None
    message_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-to-backup-dark': 'icons8_add_folder_24px.png',
            'add-to-backup-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'logo': 'backup.png'
        }

        self.photoimages = []
        imgpath = PATH + '\\assets\\'
        for key, val in image_files.items():
            _path = imgpath + val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        # buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        # new backup
        _func = lambda: self.create_new_mission()
        btn = ttk.Button(
            master=buttonbar, text='新建任务',
            image='add-to-backup-light',
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        # backup
        _func = lambda: self.mission_begin()
        mission_begin_btn = ttk.Button(
            master=buttonbar,
            text='开始任务',
            image='play',
            compound=LEFT,
            command=_func
        )

        mission_begin_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)
        self.mission_begin_btn = mission_begin_btn

        # refresh
        _func = lambda: Messagebox.ok(message='Refreshing...')
        btn = ttk.Button(
            master=buttonbar,
            text='刷新',
            image='refresh',
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        # stop
        _func = lambda: self.stop_mission()
        mission_stop_btn = ttk.Button(
            master=buttonbar,
            text='停止任务',
            image='stop-light',
            compound=LEFT,
            command=_func
        )
        mission_stop_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        self.mission_stop_btn = mission_stop_btn

        # settings
        _func = lambda: Messagebox.ok(message='Changing settings')
        btn = ttk.Button(
            master=buttonbar,
            text='设置',
            image='properties-light',
            compound=LEFT,
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        # left panel
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)

        # backup summary (collapsible)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill=X, pady=1)

        # container
        bus_frm = ttk.Frame(bus_cf, padding=1)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(
            child=bus_frm,
            title='使用教程',
            bootstyle=SECONDARY)

        notice = ttk.ScrolledText(bus_frm, width=30)
        notice.insert(ttk.INSERT, '使用教程 ----------\n\n')
        notice.insert(ttk.INSERT, '1、使用前必须安装好Chrome浏览器（谷歌浏览器），暂时不支持其他类型浏览器\n\n')
        notice.insert(ttk.INSERT, '2、点击“新建任务”，填好学校和账号等信息，点确定\n\n')
        notice.insert(ttk.INSERT, '3、再在任务栏里选中任务，点击开始任务即可\n\n')
        notice.insert(ttk.INSERT, '4、若需要删除任务，可选中任务后，单击右键再点删除\n\n')

        notice.insert(ttk.INSERT, '注意 ----------\n\n')
        notice.insert(ttk.INSERT, '1、网课网站在凌晨12点以后会将账号强制踢下线，请挑选合适的时间使用\n\n')
        notice.insert(ttk.INSERT, '2、进入到有视频的界面以后，如果视频的章节数与你之前刷的不符合，可以手动调整。\n\n')
        notice.insert(ttk.INSERT, '3、本工具仅供学习交流使用，不保证100%不会被检测，请适度使用，如有损失概不负责！\n\n')

        notice.configure(state='disabled')
        notice.pack()

        # logo
        lbl = ttk.Label(left_panel, image='logo', style='bg.TLabel')
        lbl.pack(side='bottom')

        # right panel
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Treeview
        tv = ttk.Treeview(right_panel, show='headings', height=15)
        tv.configure(columns=(
            'name', 'state', 'creation-time',
            'run-time',
        ))
        tv.column('name', stretch=True)

        for col in ['creation-time', 'run-time', 'state']:
            tv.column(col, stretch=True)

        for col in tv['columns']:
            tv.heading(col, text=col.title(), anchor=W)

        tv.pack(fill=X, pady=1)

        self.tv = tv

        def on_click_tree(event):
            item = self.tv.identify_row(event.y)
            if len(item) == 0:
                return
            self.curr_choose_index = int(item[-1]) - 1

            state = self.tv.item(item)
            print(state['values'][1])

            if state['values'][1] == '运行中':
                mission_begin_btn.config(state="disabled")
            else:
                mission_begin_btn.config(state="normal")

            self.after_scroll_text.pack_forget()
            self.scroll_text_list[self.curr_choose_index].pack(fill=BOTH, expand=True)
            self.after_scroll_text = self.scroll_text_list[self.curr_choose_index]
            print("You clicked on item:", self.curr_choose_index)

        self.tv.bind("<Button-1>", on_click_tree)

        # scrolling text output
        scroll_cf = CollapsingFrame(right_panel)
        scroll_cf.pack(fill=BOTH, expand=True)
        output_container = ttk.Frame(scroll_cf, padding=1)
        self.output_container = output_container
        _value = '任务日志'
        self.setvar('scroll-message', _value)
        st = ScrolledText(output_container)
        self.after_scroll_text = st
        st.pack(fill=BOTH, expand=True)
        scroll_cf.add(output_container, textvariable='scroll-message')

        # create right click menu
        menu = ttk.Menu(self.tv, tearoff=1)
        menu.add_command(label="新建任务", command=self.create_new_mission)
        menu.add_separator()
        menu.add_command(label="删除", command=self.mission_delete)

        def show_menu(event):
            menu.post(event.x_root, event.y_root)
        self.tv.bind("<Button-3>", show_menu)

    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)

    # def update_scroll_text(self, text, index):
    #     self.scroll_text_list[index].insert(tkinter.INSERT, text)

    def mission_begin(self):
        if len(self.mission_list) == 0:
            Messagebox.ok(message='任务列表为空')
            return

        self.mission_begin_btn.config(state="disabled")
        self.mission_stop_btn.config(state="normal")
        selected_item = self.tv.selection()[0]
        self.tv.set(selected_item, column='state', value='运行中')
        t = Thread_with_exception(f'{self.curr_choose_index}', self.mission_list, self.curr_choose_index, self.tv,
                                  self.mission_begin_btn, self.scroll_text_list,
                                  self.message_list[self.curr_choose_index], self, selected_item)
        t.daemon = True
        t.start()
        self.threading_list.append(t)

    def mission_delete(self):
        if len(self.mission_list) == 0:
            Messagebox.ok('先新建任务吧哥')
            return
        selected_item = self.tv.selection()[0]
        self.tv.delete(selected_item)
        self.mission_list.pop(self.curr_choose_index)
        self.threading_list[self.curr_choose_index].killing_self()
        self.threading_list.pop(self.curr_choose_index)
        self.message_list.pop(self.curr_choose_index)
        self.scroll_text_list.pop(self.curr_choose_index)

    def create_new_mission(self):
        mission_infor_dic = {'name': '', 'school': '', 'id': '', 'password': '', 'platform': ''}
        new_mission_window = ttk.Toplevel("新建任务", resizable=(False, False))

        new_mission_window.attributes('-topmost', True)
        DataEntryForm(new_mission_window, mission_infor_dic)
        new_mission_window.geometry(
            f'600x400+{(new_mission_window.winfo_screenwidth() - 800) // 2}+{(new_mission_window.winfo_screenheight() - 400) // 2}')
        new_mission_window.mainloop()
        print(mission_infor_dic)
        self.mission_list.append(mission_infor_dic)
        timestamp = datetime.now().strftime('%Y.%d.%m - %H:%M:%S')
        self.tv.insert('', END, values=(mission_infor_dic['name'], '待运行', timestamp, timestamp))

        logs = ScrolledText(self.output_container)
        self.scroll_text_list.append(logs)

        q = queue.Queue()
        self.message_list.append(q)

    # 已弃用
    def stop_mission(self):
        if len(self.mission_list) == 0:
            Messagebox.ok('任务列表为空')
            return

        self.mission_stop_btn.config(state="disabled")
        selected_item = self.tv.selection()[0]
        self.tv.set(selected_item, column='state', value='已停止')
        self.mission_begin_btn.config(state='normal')

        self.threading_list[self.curr_choose_index].killing_self()
        self.threading_list.pop(self.curr_choose_index)


class CollapsingFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = [
            ttk.PhotoImage(file=PATH + '\\assets\\icons8_double_up_24px.png'),
            ttk.PhotoImage(file=PATH + '\\assets\\icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child):
            return self._toggle_open_close(c)

        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])


class Thread_with_exception(threading.Thread):
    mission_list = []
    curr_choose_index = 0
    tv = None
    mission_begin_btn = None
    scroll_text_list = []
    que = None
    mainWindow = None

    def __init__(self, name, mission_list, curr_choose_index, tv, mission_begin_btn, scroll_text_list, que, mainWindow,
                 selected_item):
        threading.Thread.__init__(self)
        self.name = name
        self.mission_list = mission_list
        self.curr_choose_index = curr_choose_index
        self.tv = tv
        self.mission_begin_btn = mission_begin_btn
        self.scroll_text_list = scroll_text_list
        self.que = que
        self.mainWindow = mainWindow
        self.selected_item = selected_item

    def run(self):
        # target function of the thread class
        try:  # 用try/finally 的方式处理exception，从而kill thread
            FuckOnlineCourse.begin(self.mission_list[self.curr_choose_index])
        except NoSuchWindowException as e:
            print('任务已结束')

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def killing_self(self):
        print('杀死线程')
        thread_id = self.get_id()

        # 给线程发过去一个exceptions，线程就那边响应完就停了
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
