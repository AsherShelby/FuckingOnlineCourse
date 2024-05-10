import ttkbootstrap as ttk
from MainWindow import MainFrame


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def init_window(root):
    MainFrame(root)


if __name__ == '__main__':
    mainWindow = ttk.Window()
    mainWindow.title("Fucking网课 某学堂自动刷课 ------by ATD团队")
    center_window(mainWindow, 1360, 768)
    init_window(mainWindow)

    mainWindow.mainloop()
