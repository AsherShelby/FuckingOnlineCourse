import ttkbootstrap as ttk
from MainWindow import MainFrame


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == '__main__':
    window = ttk.Window()
    window.title("Fucking网课 v2.1 -------by 林科大涉外某神秘人士")
    center_window(window, 1360, 790)
    mainWindow = MainFrame(window)
    style = ttk.Style()
    style.configure("Treeview", rowheight=35)

    mainWindow.mainloop()
