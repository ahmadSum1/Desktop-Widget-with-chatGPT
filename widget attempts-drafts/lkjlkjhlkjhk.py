import tkinter as tk
import json

class MyWidget:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title("My Widget")
        self.parent.overrideredirect(True)
        self.parent.attributes('-topmost', True)
        self.parent.geometry("400x400")
        self.parent.bind('<Button-1>', self.on_drag_start)
        self.parent.bind('<B1-Motion>', self.on_drag_motion)
        
        # Create a label to display data
        self.data_label = tk.Label(parent, text="", font=("Arial", 24))
        self.data_label.pack(fill="both", expand=True)
        self.refresh_data()

        # Add a close button
        close_button = tk.Button(parent, text="X", bg="red", fg="white", font=("Arial", 12), command=self.close)
        close_button.pack(side="right", padx=5, pady=5)

        # Add an "always on top" checkbox
        self.always_on_top_var = tk.BooleanVar()
        always_on_top_checkbox = tk.Checkbutton(parent, text="Always on top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        always_on_top_checkbox.pack(side="left", padx=5, pady=5)

    def refresh_data(self):
        # Load data from a JSON file
        with open("data.json") as f:
            data = json.load(f)
        # Update the label's text with the data
        self.data_label.config(text=json.dumps(data, indent=4), font=("Arial", 24))

    def close(self):
        # Destroy the widget when close button is clicked
        self.parent.destroy()

    def on_drag_start(self, event):
        # Save the starting position of the widget when dragged
        self.parent.start_x = event.x
        self.parent.start_y = event.y

    def on_drag_motion(self, event):
        # Move the widget based on mouse drag motion
        x = self.parent.winfo_x() - self.parent.start_x + event.x
        y = self.parent.winfo_y() - self.parent.start_y + event.y
        self.parent.geometry(f'+{x}+{y}')

    def toggle_always_on_top(self):
        # Set the 'topmost' attribute based on the checkbox value
        self.parent.attributes('-topmost', self.always_on_top_var.get())

# Create a root window
root = tk.Tk()

# Create a widget instance
widget = MyWidget(root)

# Start the main event loop
root.mainloop()
