import tkinter as tk

class CollapsibleFrame(tk.Frame):
    def __init__(self, parent, title="Collapsible Frame", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.is_collapsed = False

        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill="x")

        self.toggle_button = tk.Button(self.header_frame, text="-", command=self.toggle_frame)
        self.toggle_button.pack(side="left")

        self.label = tk.Label(self.header_frame, text=title)
        self.label.pack(side="left", padx=10)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

    def toggle_frame(self):
        if self.is_collapsed:
            self.content_frame.pack(fill="both", expand=True)
            self.toggle_button.config(text="-")
        else:
            self.content_frame.pack_forget()
            self.toggle_button.config(text="+")
        self.is_collapsed = not self.is_collapsed

# Example usage
root = tk.Tk()

collapsible_frame = CollapsibleFrame(root, "Collapsible Frame")

# Add content to the collapsible frame
label = tk.Label(collapsible_frame.content_frame, text="This is the content of the collapsible frame.")
label.pack(padx=20, pady=20)

root.mainloop()