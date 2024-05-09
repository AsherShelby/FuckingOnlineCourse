import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText


class TextReader(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.filename = ttk.StringVar()
        self.pack(fill=BOTH, expand=YES)
        self.create_widget_elements()

    def create_widget_elements(self):
        """Create and add the widget elements"""
        style = ttk.Style()
        self.textbox = ScrolledText(
            master=self,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1
        )
        self.textbox.pack(fill=BOTH)
        default_txt = "Click the browse button to open a new text file."
        self.textbox.insert(END, default_txt)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            self.textbox.delete('1.0', END)
            self.textbox.insert(END, f.read())
            self.filename.set(path)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def init_window(root):
    frame = ttk.Frame(root, relief=tk.SOLID)
    frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    TextReader(frame)

    # data = [("hello world",) for _ in range(100)]
    # tree = ttk.Treeview(frame, columns=('id',), show="headings", displaycolumns="#all")
    # tree.heading('id', text="日志", anchor=W)
    # for itm in data:
    #     tree.insert("", END, values=itm)
    # tree.pack(expand=1, fill=BOTH, padx=25, pady=25, side=tk.LEFT)

    # message_text = tk.Text(frame, width=25, height=25)
    # message_text.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=25, pady=25)

    # button_frame = ttk.Frame(root, relief=tk.SOLID)
    # button_frame.pack(side=tk.RIGHT)
    # for i in range(5):
    #     button = ttk.Button(button_frame, text=f"Button {i + 1}")
    #     button.pack(fill=tk.X, pady=5, padx=10)


if __name__ == '__main__':
    mainWindow = tk.Tk()
    mainWindow.title("Fucking网课 某学堂自动刷课 ------by ATD团队")

    center_window(mainWindow, 800, 600)
    init_window(mainWindow)

    mainWindow.mainloop()
