from tkinter import Tk


class AdwRun(object):
    def __init__(self, root: Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def run(self):
        self.q = False
        while not self.q:
            self.root.update()

    def quit(self):
        self.q = True
        self.root.destroy()


def run(root):
    AdwRun(root).run()


if __name__ == '__main__':
    root = Tk()
    run(root)
