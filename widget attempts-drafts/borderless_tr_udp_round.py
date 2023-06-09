import requests
import tkinter as tk
import json
import math
import fjson


import sys
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

# Set the socket to non blocking, allows the program to continue and not wait for data the whole time
client.setblocking(1)

# Bind to all interfaces and to port 2255
client.bind(('', 4040))

def check_data():
    try:
        # Data received
        data, addr = client.recvfrom(1024)
        
        data_str = data.decode('utf-8')

        # Parse the JSON data and update the label
        json_data = json.loads(data_str, parse_float=lambda x: round(float(x), 2))
        
        return json_data
    # If no data is received just return None
    except socket.error:
        return None



class MyWidget:
    def __init__(self, parent):
        self.parent = parent

        # Remove the window border
        parent.overrideredirect(True)

        # Set the window alpha value to 0.5 for transparency
        parent.wm_attributes('-alpha', 0.75)

        # Create a frame with rounded corners
        self.frame = tk.Frame(parent, bg="black", bd=0, highlightthickness=0, borderwidth=10, relief="ridge")
        self.frame.pack(fill="both", expand=True)

        # Create the data label inside the frame
        self.data_label = tk.Label(self.frame, text="", bg="black", fg="white", font=("Segoe UI", 22), justify='left')
        self.data_label.pack(pady=10)

        # Create a right-click menu
        self.menu = tk.Menu(parent, tearoff=0)
        self.menu.add_command(label="Move", command=self.move_window)
        self.menu.add_command(label="Close", command=self.close_window)

        # Bind the right-click menu to the widget
        self.frame.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        # Show the right-click menu at the mouse location
        self.menu.post(event.x_root, event.y_root)

    def move_window(self):
        # Allow the user to move the window by clicking and dragging the widget
        self.frame.bind("<ButtonPress-1>", self.on_start_move)
        self.frame.bind("<ButtonRelease-1>", self.on_stop_move)
        self.frame.bind("<B1-Motion>", self.on_move)

    def on_start_move(self, event):
        # Record the current position of the widget when the user starts moving it
        self.x = event.x
        self.y = event.y

    def on_stop_move(self, event):
        # Remove the mouse bindings for moving the widget when the user stops dragging it
        self.frame.unbind("<ButtonPress-1>")
        self.frame.unbind("<ButtonRelease-1>")
        self.frame.unbind("<B1-Motion>")

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
        # Check for UDP data
        data = check_data()
        if data is not None:
            self.data_label.config(text=fjson.dumps(data, float_format=".2f", indent=4), justify='left')
            # Schedule the next refresh in 1 second
            self.parent.after(1000, self.refresh_data)
        else:
            self.parent.after(100, self.refresh_data)
            
            
# Create the main tkinter window
root = tk.Tk()



# Set the initial position of the window to the top-right corner of the screen
screen_width = root.winfo_screenwidth()
x = screen_width - root.winfo_reqwidth()
root.geometry("+%d+0" % x)

# Create the widget and add it to the window
widget = MyWidget(root)

# Start the tkinter event loop
root.mainloop()
