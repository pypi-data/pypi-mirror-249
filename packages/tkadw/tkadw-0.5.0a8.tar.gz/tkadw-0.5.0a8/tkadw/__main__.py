from tkadw import *
from tkinter import *

theme = nametotheme(
    "ant"
)
print(theme.fullpath)

window = AdwTMainWindow()
window.iconbitmap()
window.geometry("540x380")

set_default_theme(theme, "dark", window)

window.dark(True)

titlebar = customwindow(window)

menubar = create_root_themed_menubar()
bind_window_move(menubar)

mainframe = AdwTFrame(window)

AdwTButton(mainframe, text="AdwTButton").pack(fill="x", padx=10, pady=10)

AdwTEntry(mainframe).pack(fill="x", padx=10, pady=10)

AdwTDivider(mainframe).pack(fill="x", padx=10, pady=10)

AdwTCircularButton(mainframe, text="AdwTCircularButton").pack(padx=10, pady=10)

mainframe.pack(fill="both", expand="yes", padx=10, pady=10)

sizegrip = AdwTSizegrip(window)
sizegrip.pack(side="bottom", anchor="se", padx=10, pady=5)

window.mainloop()
