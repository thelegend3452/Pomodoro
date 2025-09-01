import tkinter as tk
import tkinter.messagebox
import threading
import time

class PomodoroTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("⏱ Pomodoro Timer")
        self.geometry("300x200")
        self.configure(bg='#2c3e50')
        self.resizable(False, False)
        

        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

      
        self.work_minutes = 25
        self.break_minutes = 5
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.is_running = False
        self.on_break = False
        self.timer_thread = None

        self.time_label = tk.Label(self, text=self.format_time(self.remaining), font=("Helvetica", 48, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.time_label.pack(pady=20)


        btn_frame = tk.Frame(self, bg='#2c3e50')
        btn_frame.pack(pady=10)

        self.start_btn = self.create_button(btn_frame, "Start", self.start_timer)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = self.create_button(btn_frame, "Stop", self.stop_timer)
        self.stop_btn.pack(side="left", padx=5)

        self.reset_btn = self.create_button(btn_frame, "Reset", self.reset_timer)
        self.reset_btn.pack(side="left", padx=5)

        menu_frame = tk.Frame(self, bg='#2c3e50')
        menu_frame.pack()
        
        tk.Label(menu_frame, text="Set Duration:", fg="#ecf0f1", bg="#2c3e50", font=("Helvetica", 10)).pack(side="left", padx=5)
        
        self.set_30_min_btn = self.create_button(menu_frame, "30 Min", lambda: self.set_new_time(30))
        self.set_30_min_btn.pack(side="left", padx=5)
        
        self.set_60_min_btn = self.create_button(menu_frame, "60 Min", lambda: self.set_new_time(60))
        self.set_60_min_btn.pack(side="left", padx=5)

    def create_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, font=("Helvetica", 10, "bold"), 
                         fg="#2c3e50", bg="#ecf0f1", activebackground="#bdc3c7", 
                         activeforeground="#2c3e50", bd=0, relief="flat", padx=10, pady=5)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self):
        """The main timer loop running in a separate thread."""
        while self.is_running and self.remaining > 0:
            self.remaining -= 1
            self.time_label.config(text=self.format_time(self.remaining))
            time.sleep(1)
            
        if self.remaining == 0:
            self.is_running = False
            self.after(0, self.handle_completion)

    def handle_completion(self):
        if not self.on_break:
            self.show_alert("Pomodoro", "Work session finished! Time for a break.")
            self.time_label.config(text="✅ Work done!")
            self.start_break(self.break_minutes)
        else:
            self.show_alert("Pomodoro", "Break finished! Back to work.")
            self.time_label.config(text="✅ Break over!")
            self.reset_to_work()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
            self.timer_thread.start()

    def stop_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.stop_timer()
        self.remaining = self.total_seconds
        self.time_label.config(text=self.format_time(self.remaining))

    def start_break(self, minutes):
        self.on_break = True
        self.total_seconds = minutes * 60
        self.remaining = self.total_seconds
        self.time_label.config(text=self.format_time(self.remaining))
        self.start_timer()

    def reset_to_work(self):
        self.on_break = False
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.time_label.config(text=self.format_time(self.remaining))

    def set_new_time(self, minutes):
        self.stop_timer()
        self.work_minutes = minutes
        self.total_seconds = minutes * 60
        self.remaining = self.total_seconds
        self.time_label.config(text=self.format_time(self.remaining))

    def show_alert(self, title, message):
        self.bell()
        tkinter.messagebox.showinfo(title, message)

if __name__ == "__main__":
    app = PomodoroTimer()
    app.mainloop()
