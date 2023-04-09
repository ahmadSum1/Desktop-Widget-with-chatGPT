import requests
import json
import tkinter as tk
import argparse


class MyWidget:
    def __init__(self, root, url, refresh_rate, key):
        self.root = root
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg='white')
        self.url = url
        self.refresh_rate = refresh_rate
        self.key = key
        
        # Create label to display data
        self.data_label = tk.Label(self.root, font=("Arial", 20), bg='white', fg='black')
        self.data_label.pack(expand=True)

        # Create options menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Move", command=lambda: self.bind_move())
        self.menu.add_command(label="Close", command=self.root.quit)
        self.root.bind("<Button-3>", lambda event: self.menu.post(event.x_root, event.y_root))
        
        # Position widget at top-right corner
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry('+{}+{}'.format(self.screen_width - 200, 0))

        # Refresh data
        self.refresh_data()

    def refresh_data(self):
        try:
            response = requests.get(self.url)
            data = json.loads(response.text)
            if self.key in data:
                self.data_label.config(text=data[self.key])
        except (requests.exceptions.ConnectionError, json.JSONDecodeError):
            self.data_label.config(text="Error")
        
        self.root.after(self.refresh_rate, self.refresh_data)
    
    def move_window(self, event):
        self.root.geometry(f"+{event.x_root - self.start_x}+{event.y_root - self.start_y}")

    def on_button_press(self, event):
        self.start_x = event.x_root - self.root.winfo_x()
        self.start_y = event.y_root - self.root.winfo_y()

    def on_button_release(self, event):
        pass
    
    def bind_move(self):
        self.root.bind("<ButtonPress-1>", self.on_button_press)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<B1-Motion>", self.move_window)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a desktop widget that displays data from a URL')
    parser.add_argument('--url', type=str, default='http://worldtimeapi.org/api/timezone/Europe/Oslo',
                        help='The URL to retrieve data from')
    parser.add_argument('--refresh', type=int, default=1000,
                        help='The refresh rate for updating data (in milliseconds)')
    parser.add_argument('--key', type=str, default='datetime',
                        help='The key to use for displaying data')
    args = parser.parse_args()
    
    root = tk.Tk()
    # root.overrideredirect(True)
    # root.attributes("-topmost", True)
    # root.geometry("200x50")
    
    MyWidget(root, args.url, args.refresh, args.key)
    
    root.mainloop()
