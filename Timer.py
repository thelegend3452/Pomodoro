#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rumps
import os

class TimerApp(rumps.App):
    def __init__(self):
        super().__init__("⏱ Pomodoro", icon="timer.png")
        
        self.total_seconds = 10 * 1   
        self.remaining = self.total_seconds
        self.is_running = False

        self.timer = rumps.Timer(self.update_timer, 1)

        # kontroll meny
        self.menu = [
            "Start",
            "Stopp",
            "Omstart",
            None,
            rumps.MenuItem("⏱ Sett varighet", callback=None, dimensions=(200, 25)),
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
            self.title = "✅ TIMER OVER! TAKE A BREAK!"
            self.show_alert("POMODORO", "✅TIME IS FINISHED, TAKE A WELL DESERVED BREAK!✅")

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

    # TID MENY
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


    def show_alert(self, title="⏱ Pomodoro", message="Tiden er ferdig!"):
        command = f'''
    osascript -e 'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"'
    '''
        os.system(command)


        
        

if __name__ == "__main__":
    TimerApp().run()
