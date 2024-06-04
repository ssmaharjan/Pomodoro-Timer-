import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Set the default time for work and break intervals in seconds
WORK_TIME = 1 * 60
SHORT_BREAK_TIME = 5 * 60
LONG_BREAK_TIME = 15 * 60

class PomodoroTimer:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.geometry("300x200")
        self.root.title("Pomodoro Timer")

        # Apply a dark mode theme using ttkbootstrap
        self.style = Style(theme="darkly")
        self.style.theme_use()

        # Add a label to display the timer
        self.timer_label = tk.Label(self.root, text="", font=("TkDefaultFont", 40), fg='white', bg='black')
        self.timer_label.pack(pady=20)

        # Add start and stop buttons
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Initialize timer variables
        self.reset_timer()
        self.is_running = False

        # Start the main event loop
        self.root.mainloop()

    def reset_timer(self):
        self.work_time = WORK_TIME
        self.break_time = SHORT_BREAK_TIME
        self.is_work_time = True
        self.pomodoros_completed = 0

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    self.play_sound()
                    self.show_message("Break Time", "Take a break!")
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time = True
                    self.work_time = WORK_TIME
                    self.play_sound()
                    self.show_message("Work Time", "Get back to work!")

            self.update_timer_label()
            self.root.after(1000, self.update_timer)

    def update_timer_label(self):
        time_left = self.work_time if self.is_work_time else self.break_time
        minutes, seconds = divmod(time_left, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def play_sound(self):
        # Play the custom alarm sound
        pygame.mixer.music.load("Racing into the night - Ringtone Remix.mp3")
        pygame.mixer.music.play()

PomodoroTimer()
