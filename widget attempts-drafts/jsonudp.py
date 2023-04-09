import json
import socket
import tkinter as tk

class MyWidget:
    def __init__(self, master, key="sensor", port=4040):
        self.master = master
        self.master.overrideredirect(True)
        self.master.geometry("+{}+{}".format(1500, 10))
        self.master.attributes('-transparentcolor', 'white')
        self.master.attributes('-alpha', 0.7)
        self.master.bind("<Button-3>", self.show_menu)
        
        self.key = key
        self.port = port

        self.data_label = tk.Label(self.master, text="", font=("Arial", 20), bg="white")
        self.data_label.pack()

        self.menu = tk.Menu(self.master, tearoff=0)
        self.menu.add_command(label="Move", command=self.move)
        self.menu.add_command(label="Close", command=self.close)

    def refresh_data(self):
        try:
            # Set up the UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(('0.0.0.0', self.port))

            # Receive the data and convert it from bytes to string
            data, address = self.sock.recvfrom(1024)
            data_str = data.decode('utf-8')

            # Parse the JSON data and update the label
            json_data = json.loads(data_str)
            self.data_label.config(text=json_data[self.key])
        except Exception as e:
            print("Error:", e)
            raise                 
        except KeyboardInterrupt:
            self.sock.close()
            self.quit()
            sys.exit()
            raise                 
        
        self.master.after(1000, self.refresh_data)

    def move(self, event=None):
        self.master.geometry("+{}+{}".format(event.x_root, event.y_root))

    def close(self):
        self.master.destroy()

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    root = tk.Tk()
    widget = MyWidget(root, key="Temperature", port=4040)
    widget.refresh_data()
    # root.mainloop()

    try:
        root.mainloop()
    # CTRL + C pressed so exit gracefully
    except KeyboardInterrupt:
        print('Interrupted.')
        sys.exit()