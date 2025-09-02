#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rumps
import os

class TimerApp(rumps.App):
    def __init__(self):
        super().__init__("⏱ Pomodoro", icon=("timer.png"))

        
        self.work_minutes = 25
        self.break_minutes = 1

        self.total_seconds = self.work_minutes * 60 
        self.remaining = self.total_seconds
        self.is_running = False
        self.on_break = False
        self.pomodoro_count = 0
        self.timer = rumps.Timer(self.update_timer, 1)

        # kontroll meny
        self.menu = [
            "Start",
            "Stop",
            "Restart",
            "Break",
            None,
            rumps.MenuItem("⏱ Choose Timer", callback=None, dimensions=(200, 25)),
            rumps.MenuItem("25 Minutes", callback=self.set_defaultTime),
            rumps.MenuItem("30 Minutter", callback=self.set_halfhour),
            rumps.MenuItem("60 Minutter", callback=self.set_hour),
        ]

        self.title = self.format_time(self.remaining)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def update_timer(self, _):
        if self.is_running and self.remaining > 0:
            self.remaining -= 1
            self.title = self.format_time(self.remaining)
        elif self.is_running and self.remaining == 0:
            self.timer.stop()
            self.is_running = False

            if not self.on_break:
                self.pomodoro_count += 1
                self.title = "✅ Work done! Take a break!"
                self.show_alert("Pomodoro", "Work session finished! Time for a break.")
                self.start_break(self.break_minutes)
            else:
                self.title = "✅ Break over! Back to work!"
                self.show_alert("Pomodoro", "Break finished! Back to work.")
                self.reset_to_work()
                

    # Tid kontroll
    @rumps.clicked("Start")
    def start_timer(self, _):
        if not self.is_running:
            if self.remaining == 0:
                self.reset_timer(None)
            self.is_running = True
            self.timer.start()

    @rumps.clicked("Stopp")
    def stop_timer(self, _):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            

    @rumps.clicked("Omstart")
    def reset_timer(self, _):
        self.timer.stop()
        self.is_running = False
        self.remaining = self.total_seconds
        self.title = self.format_time(self.remaining)

    # PAUSE
    def start_break(self, minutes):
        self.on_break = True
        self.total_seconds = minutes * 60
        self.remaining = self.total_seconds
        self.is_running = True
        self.timer.start()
        self.title = f"🛌 {self.format_time(self.remaining)}"

    def reset_to_work(self):
        self.on_break = False
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.is_running = True
        self.timer.start()
        self.title = self.format_time(self.remaining)

    # TID MENY
    def set_defaultTime(self,_):
        self.set_new_time(25)
    
    def set_halfhour(self, _):
        self.set_new_time(30)

    def set_hour(self, _):
        self.set_new_time(60)
        
    

    def set_new_time(self, minutes):
        self.timer.stop()
        self.is_running = False
        self.total_seconds = minutes * 60
        self.remaining = self.total_seconds
        self.title = self.format_time(self.remaining)
        
        if minutes <= 25:
            self.break_minutes = 5
        elif minutes <= 30:
            self.break_minutes = 10
        elif minutes <= 60:
            self.break_minutes = 15


    def show_alert(self, title="⏱ Pomodoro", message="GOOD JOB!"):
        command = f'''
    osascript -e 'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"'
    '''
        os.system(command)


if __name__ == "__main__":
    TimerApp().run()
