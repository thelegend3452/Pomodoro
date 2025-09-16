#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 11:10:23 2025

@author: asmaarabid
"""

import rumps
import os
import threading
from playsound import playsound

class TimerApp(rumps.App):
    def __init__(self):
        super().__init__("⏱ Pomodoro", icon=("timer.png"))
        self.status = rumps.MenuItem("Status:", callback=None)
        self.manual_break = False
        self.sound_on = True
        self.muted = False

        self.target_intervals = 0
        self.long_break = 15
        self.extra_long_break = 25
        self.extra_extra_long_break = 35

        self.work_minutes = 25
        self.break_minutes = 5
        self.amount_breaks = 0
        self.sbreak_minutes = 2

        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.is_running = False
        self.on_break = False
        self.pomodoro_count = 0
        self.timer = rumps.Timer(self.update_timer, 1)

        self.sound_path = os.path.join(os.path.dirname(__file__), "sound.mp3")

        self.choose_timer_label = rumps.MenuItem("⏱ Choose Timer", callback=None, dimensions=(200, 25))
        self.sessions_label = rumps.MenuItem("Sessions", callback=None, dimensions=(200, 25))
        self.alerts_label = rumps.MenuItem("Alerts", callback=None, dimensions=(200, 25))

        self.mute = rumps.MenuItem("Mute", callback=self.toggle_mute)
        self.sound = rumps.MenuItem("Sound", callback=self.toggle_sound)
        
        self.mute.state = False
        self.sound.state = True

        #Kontroll meny
        self.menu = [
            self.status,
            None,
            "Start",
            "Stop",
            "Restart",
            "Break",
            None,
            self.choose_timer_label,
            rumps.MenuItem("25 Minutes", callback=self.set_defaultTime),
            rumps.MenuItem("30 Minutter", callback=self.set_halfhour),
            rumps.MenuItem("60 Minutter", callback=self.set_hour),
            None,
            self.sessions_label,
            "2 Intervals",
            "4 Intervals",
            "6 Intervals",
            None,
            self.alerts_label,
            self.mute,
            self.sound,
            None,
        ]

        self.title = self.format_time(self.remaining)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def play_sound(self):
        if not (self.sound_on and not self.muted):
            return
        path = self.sound_path
        if not os.path.exists(path):
            os.path.join(os.getcwd(), "sound.mp3")
            return
        threading.Thread(target=lambda: playsound(path), daemon=True).start()

    def update_timer(self, _):
        if self.is_running and self.remaining > 0:
            self.remaining -= 1
            self.title = self.format_time(self.remaining)

        elif self.is_running and self.remaining == 0:
            self.timer.stop()
            self.is_running = False

            if not self.on_break:
                self.pomodoro_count += 1

                if self.target_intervals > 0 and self.pomodoro_count >= self.target_intervals:
                    if self.target_intervals == 2:
                        self.manual_break = False
                        self.start_break(self.long_break)
                    elif self.target_intervals == 4:
                        self.start_break(self.extra_long_break)
                    elif self.target_intervals == 6:
                        self.start_break(self.extra_extra_long_break)
                    self.title = "✅ Long break time!"
                    self.show_alert("Pomodoro", "Great job! Take a long break.")
                    self.pomodoro_count = 0
                else:
                    self.title = "✅ Work done! Take a short break!"
                    self.show_alert("Pomodoro", "Work session finished! Time for a break.")
                    self.start_break(self.break_minutes)
                    self.play_sound()

            else:
                self.title = "✅ Break over! Back to work!"
                self.show_alert("Pomodoro", "Break finished! Back to work.")
                self.play_sound()
                if self.manual_break:
                    self.resume_work()
                else:
                    self.reset_to_work()

    # Tid kontroll
    @rumps.clicked("Start")
    def start_timer(self, _):
        if not self.is_running:
            if self.remaining == 0:
                self.reset_timer(None)
            self.is_running = True
            self.timer.start()
            self.status_item.title = "Status: work"

    @rumps.clicked("Stop")
    def stop_timer(self, _):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.status_item.title = "Status: Timer stopped"

    @rumps.clicked("Restart")
    def reset_timer(self, _):
        self.timer.stop()
        self.is_running = False
        self.remaining = self.total_seconds
        self.title = self.format_time(self.remaining)

    @rumps.clicked("Break")
    def break_timer(self, _):
        self.saved_break = self.remaining
        self.start_break(self.sbreak_minutes)
        self.manual_break = True

    # SESSIONS
    @rumps.clicked("2 Intervals")
    def two_intervals(self, _):
        self.target_intervals = 2
        self.show_alert("Pomodoro", "2 intervals before a long break.")
        self.reset_to_work()
        self.is_running = True
        self.timer.start()
        self.status.title = "Status: 2 intervals"

    @rumps.clicked("4 Intervals")
    def four_intervals(self, _):
        self.target_intervals = 4
        self.show_alert("Pomodoro", "4 intervals before a long break.")
        self.reset_to_work()
        self.is_running = True
        self.timer.start()

    @rumps.clicked("6 Intervals")
    def six_intervals(self, _):
        self.target_intervals = 6
        self.show_alert("Pomodoro", "6 intervals before a long break.")
        self.reset_to_work()
        self.is_running = True
        self.timer.start()

    # PAUSE
    def start_break(self, minutes):
        self.on_break = True
        self.total_seconds = minutes * 60
        self.remaining = self.total_seconds
        self.is_running = True
        self.timer.start()
        self.title = f"🛌 {self.format_time(self.remaining)}"
        self.status.title = "Status: Break"

    def reset_to_work(self):
        self.on_break = False
        self.total_seconds = self.work_minutes * 60
        self.remaining = self.total_seconds
        self.is_running = True
        self.timer.start()
        self.title = self.format_time(self.remaining)
        self.status.title = "Status: Work"

    def resume_work(self):
        self.on_break = False
        if hasattr(self, "saved_break"):
            self.remaining = self.saved_break
        else:
            self.remaining = self.work_minutes * 60
        self.is_running = True
        self.timer.start()
        self.title = self.format_time(self.remaining)
        self.status.title = "Status: Work"

    # TID MENY
    def set_defaultTime(self, _):
        self.set_new_time(25)

    def set_halfhour(self, _):
        self.set_new_time(30)

    def set_hour(self, _):
        self.set_new_time(60)

    def toggle_sound(self, sender):
        self.sound_on = True
        self.muted = False
        self.sound.state = True
        self.mute.state = False

    def toggle_mute(self, sender):
        self.muted = True
        self.sound_on = False
        self.mute.state = True
        self.sound.state = False

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
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
        os.system(command)


if __name__ == "__main__":
    TimerApp().run()
