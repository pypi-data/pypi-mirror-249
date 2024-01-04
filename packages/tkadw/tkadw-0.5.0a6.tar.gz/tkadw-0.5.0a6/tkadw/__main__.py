from tkadw import *

window = AdwTMainWindow()
window.geometry("540x380")

theme = AdwFluentTheme()
theme.accent("darkorange", "orange")
window.theme(theme, "dark")
window.dark(True)

titlebar = AdwCustomWindow(window)

menubar = AdwTMenuBar(window)
AdwBindMove(menubar)
menubar.show()

mainframe = AdwTFrame(window)

AdwTButton(mainframe, text="AdwTButton").pack(fill="x", padx=10, pady=10)

AdwTEntry(mainframe).pack(fill="x", padx=10, pady=10)

AdwTSeparator(mainframe).pack(fill="x", padx=10, pady=10)

AdwTCircularButton(mainframe, text="AdwTCircularButton").pack(padx=10, pady=10)

mainframe.pack(fill="both", expand="yes", padx=10, pady=10)

sizegrip = AdwTSizegrip(window)
sizegrip.pack(side="bottom", anchor="se", padx=10, pady=5)

window.run()

