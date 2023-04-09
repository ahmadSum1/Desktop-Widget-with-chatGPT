import requests
import tkinter as tk

class MyWidget:
    def __init__(self, parent):
        self.parent = parent
        self.url = "http://worldtimeapi.org/api/timezone/Europe/Oslo"
        self.data_label = tk.Label(parent, text="", bg="white")
        self.data_label.pack()
        self.refresh_data()

        # Create a right-click menu
        self.menu = tk.Menu(parent, tearoff=0)
        self.menu.add_command(label="Move", command=self.move_window)
        self.menu.add_command(label="Close", command=self.close_window)

        # Bind the right-click menu to the widget
        self.data_label.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        # Show the right-click menu at the mouse location
        self.menu.post(event.x_root, event.y_root)

    def move_window(self):
        # Allow the user to move the window by clicking and dragging the widget
        self.data_label.bind("<ButtonPress-1>", self.on_start_move)
        self.data_label.bind("<ButtonRelease-1>", self.on_stop_move)
        self.data_label.bind("<B1-Motion>", self.on_move)

    def on_start_move(self, event):
        # Record the current position of the widget when the user starts moving it
        self.x = event.x
        self.y = event.y

    def on_stop_move(self, event):
        # Remove the mouse bindings for moving the widget when the user stops dragging it
        self.data_label.unbind("<ButtonPress-1>")
        self.data_label.unbind("<ButtonRelease-1>")
        self.data_label.unbind("<B1-Motion>")

    def on_move(self, event):
        # Calculate the new position of the widget based on the mouse movement
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.parent.winfo_x() + deltax
        y = self.parent.winfo_y() + deltay
        self.parent.geometry("+%s+%s" % (x, y))

    def close_window(self):
        # Close the window when the user selects the "Close" option
        self.parent.destroy()

    def refresh_data(self):
        # Make an HTTP request to the URL
        response = requests.get(self.url)
        # Extract the data from the response
        data = response.json()
        # Check if the key exists in the data dictionary
        if "utc_datetime" in data:
            # Update the label with the data
            self.data_label.config(text=data["utc_datetime"])
        else:
            # Handle the case where the key does not exist
            self.data_label.config(text="Key not found")
        # Schedule the next refresh in 1 second
        self.parent.after(1000, self.refresh_data)

# Create the main tkinter window
root = tk.Tk()

# Remove the window border
root.overrideredirect(True)

# Set the window alpha value to 0.5 for transparency
root.wm_attributes('-alpha', 0.5)

# Create the widget and add it to the window
widget = MyWidget(root)

# Start the tkinter event loop
root.mainloop()
