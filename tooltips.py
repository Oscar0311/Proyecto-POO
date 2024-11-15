import tkinter as tk

class tooltips:
    def __init__(self, widget, text):
        self.__widget = widget
        self.__text = text
        self.__tooltip_window = None
        # Bind events for showing and hiding the tooltip
        widget.bind("<Enter>", self.__show_tooltip)
        widget.bind("<Leave>", self.__hide_tooltip)

    def __show_tooltip(self, event):
        if self.__tooltip_window or not self.__text:
            return
        # Position the tooltip near the mouse
        x = event.x_root + 20
        y = event.y_root + 10
        self.__tooltip_window = tw = tk.Toplevel(self.__widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.__text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", 10, "normal"))
        label.pack(ipadx=1)

    def __hide_tooltip(self, event):
        if self.__tooltip_window:
            self.__tooltip_window.destroy()
            self.__tooltip_window = None