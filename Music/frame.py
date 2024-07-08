import tkinter as tk

class Window:
    def __init__(self, parent, frame_name):
        self.parent = parent
        self.dialogue = tk.Toplevel(parent)
        self.dialogue.title(f"{frame_name} Dialogue")
        self.dialogue.geometry("809x500")
        self.dialogue.configure(bg="#c90076")

        self.dialogue.protocol("WM_DELETE_WINDOW", self.on_close)
        parent.withdraw()
        self.center_window()

    def on_close(self):
        self.dialogue.destroy()
        self.parent.deiconify()

    def center_window(self):
        self.dialogue.update_idletasks()
        width = self.dialogue.winfo_width()
        height = self.dialogue.winfo_height()
        x = (self.dialogue.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialogue.winfo_screenheight() // 2) - (height // 2)
        self.dialogue.geometry(f'{width}x{height}+{x}+{y}')
        self.dialogue.deiconify()
        self.dialogue.focus_set()
        self.dialogue.attributes('-topmost', True)
        self.dialogue.after(1, lambda: self.dialogue.attributes('-topmost', False))
