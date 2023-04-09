import tkinter as tk
import socket
import json

class MyWidget:
    def __init__(self, parent):
        self.parent = parent
        self.port = 4040
        self.data_label = tk.Label(parent, text="", bg="white")
        self.data_label.pack()
        self.refresh_data()

    def refresh_data(self):
        try:
            # Set up the UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', self.port))

            # Receive the data and convert it from bytes to string
            data, address = sock.recvfrom(1024)
            data_str = data.decode('utf-8')

            # Parse the JSON data and update the label
            json_data = json.loads(data_str)
            # self.data_label.config(text=json_data["Temperature"])
            
            # # Clear any existing labels
            # for child in self.data_label.winfo_children():
            #     child.destroy()
            
            # Create a new label for each key-value pair in the JSON
            for key, value in json_data.items():
                label = tk.Label(self.data_label, text=f"{key}: {value}", bg="white")
                label.pack()
            
            # Schedule the next refresh in 1 second
            # self.parent.after(1000, self.refresh_data)  
            
            
        except Exception as e:
            print("Error:", e)
        finally:
            sock.close()

        self.parent.after(1000, self.refresh_data)

# Create the main tkinter window
root = tk.Tk()

# Remove the window border
root.overrideredirect(True)

# Set the window alpha value to 0.5 for transparency
root.wm_attributes('-alpha', 0.5)

# Set the initial position of the window to the top-right corner of the screen
screen_width = root.winfo_screenwidth()
x = screen_width - root.winfo_reqwidth()
root.geometry("+%d+0" % x)

# Create the widget and add it to the window
widget = MyWidget(root)

# Start the tkinter event loop
root.mainloop()
