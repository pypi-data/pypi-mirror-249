if __name__ == '__main__':
    from tkadw4 import *
    root = Adwite(dark=False)
    root.geometry("600x300")
    root.set_default_theme("win11", "system")
    #root.style_dark_with_icon(True)
    #root.style("aero")
    root.style_header("#202020")


    def command():
        widgets_panel.show_page(choose_panel.select())


    def switch_theme(event):
        print(event)
        root.set_default_theme("win11", root.get_system_theme())


    root.bind("<<SystemThemeSwitch>>", switch_theme)

    choose_panel = AdwTListBox(
        items=sorted(
            ["AdwTButton", "AdwTCircularButton", "AdwTDesignerFrame", "AdwTEntry", "AdwTMDI", "AdwTTabs"]
        ),
        item_selected=command
    )
    choose_panel.column(expand=False)

    widgets_panel = AdwTStack()
    widgets_panel.column()

    # AdwTButton
    button_panel = AdwTFrame(widgets_panel.frame)
    button = AdwTButton(button_panel.frame, text="AdwTButton")
    button.row(expand="no")
    widgets_panel.add_page(button_panel, "AdwTButton")

    # AdwTCircularButton
    cbutton_panel = AdwTFrame(widgets_panel.frame)
    cbutton = AdwTCircularButton(cbutton_panel.frame, text="AdwTCircularButton")
    cbutton.row(expand="no", fill="none")
    widgets_panel.add_page(cbutton_panel, "AdwTCircularButton")

    # AdwTDesignerFrame
    designerframe_panel = AdwTFrame(widgets_panel.frame)
    designerframe = AdwTDesignerFrame(designerframe_panel.frame, widget=AdwTButton, text="AdwTDesignerFrame")
    designerframe.place(x=5, y=5, width=160, height=60)
    widgets_panel.add_page(designerframe_panel, "AdwTDesignerFrame")

    # AdwTEntry
    entry_panel = AdwTFrame(widgets_panel.frame)
    entry = AdwTEntry(entry_panel.frame)
    entry.row(expand="no")
    widgets_panel.add_page(entry_panel, "AdwTEntry")

    # AdwTMDI
    mdi_panel = AdwTFrame(widgets_panel.frame)
    mdi = AdwTMDI(mdi_panel.frame)
    mdi_child1 = mdi.create_child()
    mdi_child2 = mdi.create_designer_child()
    mdi.row()
    widgets_panel.add_page(mdi_panel, "AdwTMDI")

    # AdwTTabs
    tabs = AdwTTabs(widgets_panel.frame)
    for i in range(5):
        f = AdwTFrame(tabs.tab_pages.frame)
        l = AdwTLabel(f.frame, text=i)
        l.row()
        tabs.add(f, f"AdwTTab {i}")
    tabs.row()
    widgets_panel.add_page(tabs, "AdwTTabs")

    choose_panel.select("AdwTButton")
    widgets_panel.show_page("AdwTButton")

    #win = Adwitew()

    root.mainloop()
