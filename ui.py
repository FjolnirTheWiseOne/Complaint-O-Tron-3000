import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import json
import os
import sys

# Define the new color palette
COLORS = {
    "bg_main": "#2E3440",        # Main background
    "bg_secondary": "#3B4252",   # Secondary background for frames
    "text_primary": "#D8DEE9",   # Primary text color
    "text_secondary": "#88C0D0", # Secondary text (labels, headings)
    "button_default": "#5E81AC", # Button background
    "button_active": "#81A1C1",  # Button hover/active background
    "accent": "#A3BE8C",         # Accent color (decorations)
    "error": "#BF616A",          # Error/warning text
}

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, callback):
        """Initialize the welcome animation screen with original colors."""
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.callback = callback
        self.create_widgets()
        self.animate()

    def create_widgets(self):
        """Create the canvas for the animation."""
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.text = "Welcome to Complaint-O-Tron 3000!"
        self.text_objects = []
        self.char_positions = []

    def animate(self):
        """Animate the welcome text with sequential letter bounces."""
        self.canvas.delete("all")
        self.text_objects = []
        self.char_positions = []
        x_start = 200
        y = 300
        font_size = 24

        for i, char in enumerate(self.text):
            text_obj = self.canvas.create_text(
                x_start + i * 15, y, text=char, font=("Courier", font_size, "bold"),
                fill="#00FF7F", anchor="center"
            )
            self.text_objects.append(text_obj)
            self.char_positions.append(y)

        self.current_letter = 0
        self.animate_letter()

    def animate_letter(self):
        """Animate the current letter with a bounce effect."""
        if self.current_letter >= len(self.text_objects):
            self.master.after(50, self.callback)
            return

        text_obj = self.text_objects[self.current_letter]
        y = self.char_positions[self.current_letter]

        def bounce(step=0):
            if step > 5:
                self.current_letter += 1
                self.master.after(50, self.animate_letter)
                return
            offset = -abs(2.5 - step) * 5
            self.canvas.coords(text_obj, self.canvas.coords(text_obj)[0], y + offset)
            self.master.after(20, lambda: bounce(step + 1))

        bounce()

class LoginScreen(tk.Frame):
    def __init__(self, parent, login_callback, data_handler):
        """Initialize the login screen with a modern aesthetic."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.login_callback = login_callback
        self.data_handler = data_handler
        self.create_widgets()

    def create_widgets(self):
        """Create login screen widgets with improved styling and centering."""
        # Main container frame to center everything
        main_frame = tk.Frame(self, bg=COLORS["bg_main"])
        main_frame.pack(expand=True)

        # Title
        title_frame = tk.Frame(main_frame, bg=COLORS["bg_main"])
        title_frame.pack(pady=30)
        tk.Label(
            title_frame, text="Complaint-O-Tron 3000",
            font=("Courier", 28, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        ).pack()

        # Main content
        content_frame = tk.Frame(main_frame, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(padx=50, pady=20)

        tk.Label(
            content_frame, text="Username:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)
        self.username_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.username_entry.pack(pady=5, padx=50, fill="x")
        self.username_entry.insert(0, "mod1")  # Pre-fill for demo purposes

        tk.Label(
            content_frame, text="Password:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)
        self.password_entry = tk.Entry(content_frame, show="*", bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.password_entry.pack(pady=5, padx=50, fill="x")
        self.password_entry.insert(0, "modpass1")  # Pre-fill for demo purposes

        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        button_frame.pack(pady=20)
        tk.Button(
            button_frame, text="Login",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.handle_login
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Register",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.show_registration
        ).pack(side="left", padx=10)

    def handle_login(self):
        """Process login button click."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.password_entry.delete(0, tk.END)
            self.login_callback(username, password)
        else:
            messagebox.showerror("Error", "Please enter both username and password", parent=self)

    def show_registration(self):
        """Redirect to the registration screen."""
        self.destroy()
        RegistrationScreen(self.master, self.login_callback, self.data_handler)

class RegistrationScreen(tk.Frame):
    def __init__(self, parent, login_callback, data_handler):
        """Initialize the registration screen with updated styling."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.login_callback = login_callback
        self.data_handler = data_handler
        self.create_widgets()

    def create_widgets(self):
        """Create registration screen widgets with improved styling and centering."""
        main_frame = tk.Frame(self, bg=COLORS["bg_main"])
        main_frame.pack(expand=True)

        tk.Label(
            main_frame, text="Register New User",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        ).pack(pady=30)

        content_frame = tk.Frame(main_frame, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(padx=50, pady=20)

        tk.Label(
            content_frame, text="Username:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.username_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.username_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Password:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.password_entry = tk.Entry(content_frame, show="*", bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.password_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Confirm Password:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.confirm_password_entry = tk.Entry(content_frame, show="*", bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.confirm_password_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Email:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.email_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.email_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Phone Number:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.phone_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.phone_entry.pack(pady=5, padx=50, fill="x")

        button_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        button_frame.pack(pady=20)
        tk.Button(
            button_frame, text="Register",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.handle_registration
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Back to Login",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.back_to_login
        ).pack(side="left", padx=10)

    def handle_registration(self):
        """Process registration submission with contact info."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if not all([username, password, confirm_password, email, phone]):
            messagebox.showerror("Error", "Please fill all fields", parent=self)
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match", parent=self)
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address", parent=self)
            return

        if not phone.replace("-", "").isdigit() or len(phone.replace("-", "")) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number", parent=self)
            return

        user_data = self.data_handler.get_user_data()
        if any(user['username'] == username for user in user_data):
            messagebox.showerror("Error", "Username already exists", parent=self)
            return

        self.data_handler.register_user(username, password, email, phone)
        messagebox.showinfo("Success", "Registration successful! Please login.", parent=self)
        self.back_to_login()

    def back_to_login(self):
        """Redirect back to the login screen."""
        self.destroy()
        LoginScreen(self.master, self.login_callback, self.data_handler)

class ProfileScreen(tk.Frame):
    def __init__(self, parent, user, data_handler, logout_callback):
        """Initialize the profile screen for viewing and editing user information."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.user = user
        self.data_handler = data_handler
        self.logout_callback = logout_callback
        self.create_widgets()

    def create_widgets(self):
        """Create profile screen widgets with improved styling and centering."""
        # Top bar
        top_frame = tk.Frame(self, bg=COLORS["bg_main"])
        top_frame.pack(fill="x", pady=10)

        welcome_label = tk.Label(
            top_frame, text=f"Welcome, {self.user['username']}!",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        )
        welcome_label.pack(side="left", padx=20)

        tk.Button(
            top_frame, text="Logout",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.logout
        ).pack(side="right", padx=20)

        # Left banner with ad joke, now with wrapping
        banner_frame = tk.Frame(self, bg=COLORS["bg_secondary"], width=250)
        banner_frame.pack(side="left", fill="y", padx=10, pady=10)
        banner_frame.pack_propagate(False)
        tk.Label(
            banner_frame, text="This could've been your ad!\nCall 1-800-ADSPACE to\nclaim this spot! 🚀",
            font=("Courier", 14, "bold"), fg=COLORS["accent"], bg=COLORS["bg_secondary"],
            justify="center", wraplength=220  # Wrap text within 220px to fit the 250px width with padding
        ).pack(expand=True)

        # Main content
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(padx=50, pady=20, expand=True)

        tk.Label(
            content_frame, text="Your Profile",
            font=("Courier", 16, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)

        tk.Label(
            content_frame, text=f"Username: {self.user['username']}",
            font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)

        tk.Label(
            content_frame, text="Email:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.email_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.email_entry.insert(0, self.user['email'])
        self.email_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Phone Number:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.phone_entry = tk.Entry(content_frame, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.phone_entry.insert(0, self.user['phone'])
        self.phone_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="New Password (leave blank to keep current):",
            font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.password_entry = tk.Entry(content_frame, show="*", bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.password_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(
            content_frame, text="Confirm New Password:",
            font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.confirm_password_entry = tk.Entry(content_frame, show="*", bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.confirm_password_entry.pack(pady=5, padx=50, fill="x")

        button_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        button_frame.pack(pady=20)
        tk.Button(
            button_frame, text="Update Profile",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.update_profile
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Back to Home",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.back_to_home
        ).pack(side="left", padx=10)

    def update_profile(self):
        """Update the user's profile information."""
        new_email = self.email_entry.get()
        new_phone = self.phone_entry.get()
        new_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not new_email or not new_phone:
            messagebox.showerror("Error", "Email and phone number are required", parent=self)
            return

        if "@" not in new_email or "." not in new_email:
            messagebox.showerror("Error", "Please enter a valid email address", parent=self)
            return

        if not new_phone.replace("-", "").isdigit() or len(new_phone.replace("-", "")) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number", parent=self)
            return

        if new_password or confirm_password:
            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match", parent=self)
                return
        else:
            new_password = None

        try:
            updated_user = self.data_handler.update_user_info(
                self.user['username'],
                new_email=new_email,
                new_phone=new_phone,
                new_password=new_password
            )
            self.user.update(updated_user)
            messagebox.showinfo("Success", "Profile updated successfully!", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def logout(self):
        """Handle logout by destroying the current screen before calling the callback."""
        self.destroy()
        self.logout_callback()

    def back_to_home(self):
        """Redirect back to the home screen."""
        self.destroy()
        HomeScreen(self.master, self.user, self.data_handler, self.logout_callback)

class HomeScreen(tk.Frame):
    def __init__(self, parent, user, data_handler, logout_callback):
        """Initialize the user home screen with updated styling."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.user = user
        self.data_handler = data_handler
        self.logout_callback = logout_callback
        self.create_widgets()

    def create_widgets(self):
        """Create home screen widgets with improved centering."""
        # Top bar
        top_frame = tk.Frame(self, bg=COLORS["bg_main"])
        top_frame.pack(fill="x", pady=10)

        welcome_label = tk.Label(
            top_frame, text=f"Welcome, {self.user['username']}!",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        )
        welcome_label.pack(side="left", padx=20)

        tk.Button(
            top_frame, text="Logout",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.logout
        ).pack(side="right", padx=20)

        # Left banner with ad joke, now with wrapping
        banner_frame = tk.Frame(self, bg=COLORS["bg_secondary"], width=250)
        banner_frame.pack(side="left", fill="y", padx=10, pady=10)
        banner_frame.pack_propagate(False)
        tk.Label(
            banner_frame, text="This could've been your ad!\nCall 1-800-ADSPACE to\nclaim this spot! 🚀",
            font=("Courier", 14, "bold"), fg=COLORS["accent"], bg=COLORS["bg_secondary"],
            justify="center", wraplength=220  # Wrap text within 220px to fit the 250px width with padding
        ).pack(expand=True)

        # Main content
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(padx=50, pady=20, expand=True)

        tk.Button(
            content_frame, text="Submit a Complaint",
            font=("Courier", 16, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=20,
            command=self.show_submit_complaint
        ).pack(pady=15)
        tk.Button(
            content_frame, text="View My Complaints",
            font=("Courier", 16, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=20,
            command=self.show_view_complaints
        ).pack(pady=15)
        tk.Button(
            content_frame, text="Profile",
            font=("Courier", 16, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=20,
            command=self.show_profile
        ).pack(pady=15)

    def logout(self):
        """Handle logout by destroying the current screen before calling the callback."""
        self.destroy()
        self.logout_callback()

    def show_submit_complaint(self):
        """Redirect to the submit complaint screen."""
        self.destroy()
        SubmitComplaintScreen(self.master, self.user, self.data_handler, self.logout_callback)

    def show_view_complaints(self):
        """Redirect to the view complaints screen."""
        self.destroy()
        ViewComplaintsScreen(self.master, self.user, self.data_handler, self.logout_callback)

    def show_profile(self):
        """Redirect to the profile screen."""
        self.destroy()
        ProfileScreen(self.master, self.user, self.data_handler, self.logout_callback)

class SubmitComplaintScreen(tk.Frame):
    def __init__(self, parent, user, data_handler, logout_callback):
        """Initialize the complaint submission screen with updated styling."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.user = user
        self.data_handler = data_handler
        self.logout_callback = logout_callback
        # Determine the base directory (same as DataHandler)
        self.base_dir = self.get_base_dir()
        self.weights_file = os.path.join(self.base_dir, "severity_weights.json")
        self.load_weights()
        self.create_widgets()

    def get_base_dir(self):
        """Get the base directory of the application (where the .exe is located)."""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def load_weights(self):
        """Load keyword weights from a JSON file, or initialize with defaults."""
        default_weights = {
            "urgent": 5.0, "emergency": 5.0, "critical": 5.0, "terrible": 4.5, "awful": 4.5,
            "bad": 4.0, "poor": 3.0, "issue": 3.0, "problem": 3.0, "minor": 2.0, "small": 1.0,
            "not a big deal": 1.0, "horrible": 4.5, "disaster": 5.0, "annoying": 3.0, "frustrating": 3.5
        }
        if os.path.exists(self.weights_file):
            with open(self.weights_file, 'r') as f:
                self.keyword_weights = json.load(f)
        else:
            self.keyword_weights = default_weights
            with open(self.weights_file, 'w') as f:
                json.dump(self.keyword_weights, f)

    def save_weights(self):
        """Save updated keyword weights to the JSON file."""
        with open(self.weights_file, 'w') as f:
            json.dump(self.keyword_weights, f)

    def create_widgets(self):
        """Create complaint submission widgets with updated styling and centering."""
        # Top bar
        top_frame = tk.Frame(self, bg=COLORS["bg_main"])
        top_frame.pack(fill="x", pady=10)

        welcome_label = tk.Label(
            top_frame, text=f"Welcome, {self.user['username']}!",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        )
        welcome_label.pack(side="left", padx=20)

        tk.Button(
            top_frame, text="Logout",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.logout
        ).pack(side="right", padx=20)

        # Left banner with ad joke, now with wrapping
        banner_frame = tk.Frame(self, bg=COLORS["bg_secondary"], width=250)
        banner_frame.pack(side="left", fill="y", padx=10, pady=10)
        banner_frame.pack_propagate(False)
        tk.Label(
            banner_frame, text="This could've been your ad!\nCall 1-800-ADSPACE to\nclaim this spot! 🚀",
            font=("Courier", 14, "bold"), fg=COLORS["accent"], bg=COLORS["bg_secondary"],
            justify="center", wraplength=220  # Wrap text within 220px to fit the 250px width with padding
        ).pack(expand=True)

        # Main content
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(padx=50, pady=20, expand=True)

        tk.Label(
            content_frame, text="Submit a Complaint",
            font=("Courier", 16, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)

        tk.Label(
            content_frame, text="Category:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.category_var = tk.StringVar()
        categories = ["Product", "Service", "Billing", "Other"]
        ttk.Combobox(content_frame, textvariable=self.category_var, values=categories, width=30).pack(pady=5)

        tk.Label(
            content_frame, text="Severity (1-5):", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        severity_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        severity_frame.pack(pady=5)
        self.severity_var = tk.StringVar()
        ttk.Combobox(
            severity_frame, textvariable=self.severity_var, values=[1, 2, 3, 4, 5], width=5
        ).pack(side="left", padx=5)
        tk.Button(
            severity_frame, text="Suggest Severity",
            font=("Courier", 12, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.suggest_severity
        ).pack(side="left", padx=5)

        tk.Label(
            content_frame, text="Description:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(pady=5)
        self.description_text = tk.Text(content_frame, height=5, width=50, bg=COLORS["bg_main"], fg=COLORS["text_primary"], font=("Courier", 12), insertbackground=COLORS["text_primary"])
        self.description_text.pack(pady=5)

        button_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        button_frame.pack(pady=20)
        tk.Button(
            button_frame, text="Submit Complaint",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.submit_complaint
        ).pack(side="left", padx=10)
        tk.Button(
            button_frame, text="Back to Home",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.back_to_home
        ).pack(side="left", padx=10)

    def suggest_severity(self):
        """Use AI to suggest a severity level based on the description."""
        description = self.description_text.get("1.0", tk.END).strip()
        if not description:
            messagebox.showerror("Error", "Please enter a description to get a severity suggestion.", parent=self)
            return

        description_lower = description.lower()
        total_score = 0.0
        matched_keywords = []

        for keyword, weight in self.keyword_weights.items():
            if keyword in description_lower:
                total_score += weight
                matched_keywords.append(keyword)

        if matched_keywords:
            suggested_severity = min(5, max(1, round(total_score / len(matched_keywords))))
        else:
            suggested_severity = 1

        self.severity_var.set(suggested_severity)
        messagebox.showinfo("AI Suggestion", f"AI suggests severity level: {suggested_severity}\nYou can adjust if needed.", parent=self)

    def update_weights(self, description, user_severity):
        """Update keyword weights based on user feedback."""
        description_lower = description.lower()
        suggested_severity = int(self.severity_var.get())
        user_severity = int(user_severity)

        if user_severity != suggested_severity:
            for keyword, weight in self.keyword_weights.items():
                if keyword in description_lower:
                    adjustment = (user_severity - suggested_severity) * 0.1
                    self.keyword_weights[keyword] = max(1.0, min(5.0, weight + adjustment))
            self.save_weights()

    def submit_complaint(self):
        """Handle complaint submission with date and update AI weights."""
        category = self.category_var.get()
        severity = self.severity_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        if category and severity and description:
            self.update_weights(description, severity)
            self.data_handler.add_complaint(self.user['username'], category, int(severity), description)
            messagebox.showinfo("Success", "Complaint submitted!", parent=self)
            self.description_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please fill all fields", parent=self)

    def logout(self):
        """Handle logout by destroying the current screen before calling the callback."""
        self.destroy()
        self.logout_callback()

    def back_to_home(self):
        """Redirect back to the home screen."""
        self.destroy()
        HomeScreen(self.master, self.user, self.data_handler, self.logout_callback)

class ViewComplaintsScreen(tk.Frame):
    def __init__(self, parent, user, data_handler, logout_callback):
        """Initialize the view complaints screen with updated styling."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.user = user
        self.data_handler = data_handler
        self.logout_callback = logout_callback
        self.sort_column = None
        self.sort_reverse = False
        self.create_widgets()

    def create_widgets(self):
        """Create view complaints widgets with improved centering."""
        # Top bar
        top_frame = tk.Frame(self, bg=COLORS["bg_main"])
        top_frame.pack(fill="x", pady=10)

        welcome_label = tk.Label(
            top_frame, text=f"Welcome, {self.user['username']}!",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        )
        welcome_label.pack(side="left", padx=20)

        tk.Button(
            top_frame, text="Logout",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.logout
        ).pack(side="right", padx=20)

        # Left banner with ad joke, now with wrapping
        banner_frame = tk.Frame(self, bg=COLORS["bg_secondary"], width=250)
        banner_frame.pack(side="left", fill="y", padx=10, pady=10)
        banner_frame.pack_propagate(False)
        tk.Label(
            banner_frame, text="This could've been your ad!\nCall 1-800-ADSPACE to\nclaim this spot! 🚀",
            font=("Courier", 14, "bold"), fg=COLORS["accent"], bg=COLORS["bg_secondary"],
            justify="center", wraplength=220  # Wrap text within 220px to fit the 250px width with padding
        ).pack(expand=True)

        # Main content
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)

        tk.Label(
            content_frame, text="Your Complaints",
            font=("Courier", 16, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)

        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", background=COLORS["bg_main"], foreground=COLORS["text_primary"], fieldbackground=COLORS["bg_main"])
        style.configure("Treeview.Heading", background=COLORS["button_default"], foreground=COLORS["text_primary"], font=("Courier", 12, "bold"))

        self.complaint_tree = ttk.Treeview(
            content_frame, columns=("ID", "Category", "Severity", "Description", "Status", "Date"),
            show="headings"
        )
        self.complaint_tree.heading("ID", text="ID")
        self.complaint_tree.heading("Category", text="Category")
        self.complaint_tree.heading("Severity", text="Severity")
        self.complaint_tree.heading("Description", text="Description")
        self.complaint_tree.heading("Status", text="Status")
        self.complaint_tree.heading("Date", text="Date")
        self.complaint_tree.configure(height=5)

        for col in self.complaint_tree["columns"]:
            self.complaint_tree.heading(col, command=lambda c=col: self.sort_by(c))

        self.complaint_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_complaints()

        tk.Button(
            content_frame, text="Back to Home",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.back_to_home
        ).pack(pady=10)

    def load_complaints(self):
        """Load user's complaints into the table, or show a placeholder if empty."""
        for item in self.complaint_tree.get_children():
            self.complaint_tree.delete(item)
        complaints = self.data_handler.get_user_complaints(self.user['username'])
        if not complaints:
            self.complaint_tree.insert("", tk.END, values=("No complaints yet", "", "", "", "", ""))
        else:
            if self.sort_column:
                complaints.sort(key=lambda x: x[self.sort_column.lower()], reverse=self.sort_reverse)
            for complaint in complaints:
                self.complaint_tree.insert("", tk.END, values=(
                    complaint['id'], complaint['category'], complaint['severity'],
                    complaint['description'][:50] + "..." if len(complaint['description']) > 50 else complaint['description'],
                    complaint['status'], complaint['date']
                ))

    def sort_by(self, column):
        """Sort the table by the clicked column."""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.load_complaints()

    def logout(self):
        """Handle logout by destroying the current screen before calling the callback."""
        self.destroy()
        self.logout_callback()

    def back_to_home(self):
        """Redirect back to the home screen."""
        self.destroy()
        HomeScreen(self.master, self.user, self.data_handler, self.logout_callback)

class ModeratorScreen(tk.Frame):
    def __init__(self, parent, data_handler, ml_models, logout_callback):
        """Initialize the moderator dashboard with updated styling."""
        super().__init__(parent, bg=COLORS["bg_main"])
        self.pack(fill="both", expand=True)
        self.data_handler = data_handler
        self.ml_models = ml_models
        self.logout_callback = logout_callback
        self.sort_column = None
        self.sort_reverse = False
        self.create_widgets()

    def create_widgets(self):
        """Create moderator screen widgets with improved centering."""
        # Top bar
        title_frame = tk.Frame(self, bg=COLORS["bg_main"])
        title_frame.pack(fill="x", pady=10)
        tk.Label(
            title_frame, text="Moderator Dashboard",
            font=("Courier", 24, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_main"]
        ).pack(side="left", padx=20)

        tk.Button(
            title_frame, text="Logout",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.logout
        ).pack(side="right", padx=20)

        # Main content
        content_frame = tk.Frame(self, bg=COLORS["bg_secondary"], padx=20, pady=20, relief="groove", bd=2)
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)

        tk.Label(
            content_frame, text="All Complaints",
            font=("Courier", 16, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)

        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", background=COLORS["bg_main"], foreground=COLORS["text_primary"], fieldbackground=COLORS["bg_main"])
        style.configure("Treeview.Heading", background=COLORS["button_default"], foreground=COLORS["text_primary"], font=("Courier", 12, "bold"))

        self.complaint_tree = ttk.Treeview(
            content_frame, columns=("ID", "Username", "Category", "Severity", "Description", "Status", "Date"),
            show="headings"
        )
        self.complaint_tree.heading("ID", text="ID")
        self.complaint_tree.heading("Username", text="Username")
        self.complaint_tree.heading("Category", text="Category")
        self.complaint_tree.heading("Severity", text="Severity")
        self.complaint_tree.heading("Description", text="Description")
        self.complaint_tree.heading("Status", text="Status")
        self.complaint_tree.heading("Date", text="Date")

        for col in self.complaint_tree["columns"]:
            self.complaint_tree.heading(col, command=lambda c=col: self.sort_by(c))

        self.complaint_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_complaints()

        tk.Label(
            content_frame, text="Update Complaint Status",
            font=("Courier", 16, "bold"), fg=COLORS["text_secondary"], bg=COLORS["bg_secondary"]
        ).pack(pady=10)

        status_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"])
        status_frame.pack(pady=5)
        tk.Label(
            status_frame, text="Complaint ID:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(side="left", padx=5)
        self.complaint_id_entry = tk.Entry(status_frame, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"], font=("Courier", 14), insertbackground=COLORS["text_primary"])
        self.complaint_id_entry.pack(side="left", padx=5)

        tk.Label(
            status_frame, text="New Status:", font=("Courier", 14), fg=COLORS["text_primary"], bg=COLORS["bg_secondary"]
        ).pack(side="left", padx=5)
        self.status_var = tk.StringVar()
        ttk.Combobox(status_frame, textvariable=self.status_var, values=["Open", "In Progress", "Resolved"], width=15).pack(side="left", padx=5)

        tk.Button(
            content_frame, text="Update Status",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.update_status
        ).pack(pady=10)

        tk.Button(
            content_frame, text="Show AI Insights",
            font=("Courier", 14, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat", width=15,
            command=self.show_ai_insights
        ).pack(pady=10)

    def load_complaints(self):
        """Load all complaints into the table."""
        for item in self.complaint_tree.get_children():
            self.complaint_tree.delete(item)
        complaints = self.data_handler.get_all_complaints()
        if self.sort_column:
            complaints.sort(key=lambda x: x[self.sort_column.lower()], reverse=self.sort_reverse)
        for complaint in complaints:
            self.complaint_tree.insert("", tk.END, values=(
                complaint['id'], complaint['username'], complaint['category'], complaint['severity'],
                complaint['description'][:50] + "..." if len(complaint['description']) > 50 else complaint['description'],
                complaint['status'], complaint['date']
            ))

    def sort_by(self, column):
        """Sort the table by the clicked column."""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.load_complaints()

    def update_status(self):
        """Update the status of a complaint."""
        complaint_id = self.complaint_id_entry.get()
        new_status = self.status_var.get()
        if complaint_id and new_status:
            try:
                self.data_handler.update_complaint_status(int(complaint_id), new_status)
                messagebox.showinfo("Success", "Status updated!", parent=self)
                self.load_complaints()
            except ValueError:
                messagebox.showerror("Error", "Invalid Complaint ID", parent=self)
        else:
            messagebox.showerror("Error", "Please enter Complaint ID and select a status", parent=self)

    def logout(self):
        """Handle logout by destroying the current screen before calling the callback."""
        self.destroy()
        self.logout_callback()

    def show_ai_insights(self):
        """Display an interactive AI insights window with buttons for different analyses."""
        insights_window = tk.Toplevel(self)
        insights_window.title("AI Insights")
        insights_window.geometry("800x600")
        insights_window.configure(bg=COLORS["bg_main"])

        button_frame = tk.Frame(insights_window, bg=COLORS["bg_main"])
        button_frame.pack(fill="x", pady=10)

        result_frame = tk.Frame(insights_window, bg=COLORS["bg_main"])
        result_frame.pack(fill="x", pady=5)
        self.result_label = tk.Label(
            result_frame, text="Select an analysis to view results",
            font=("Courier", 12), fg=COLORS["text_primary"], bg=COLORS["bg_main"], justify="left"
        )
        self.result_label.pack(anchor="w", padx=10)

        plot_frame = tk.Frame(insights_window, bg=COLORS["bg_main"])
        plot_frame.pack(fill="both", expand=True, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(
            button_frame, text="Predict Urgency",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_urgency
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Cluster Complaints",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_clusters
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Predict Resolution Time",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_resolution_time
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Analyze Sentiment",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_sentiment
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Detect Anomalies",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_anomalies
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Plot Trends",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_trends
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Plot Categories",
            font=("Courier", 10, "bold"), fg=COLORS["text_primary"], bg=COLORS["button_default"],
            activebackground=COLORS["button_active"], relief="flat",
            command=self.show_categories
        ).pack(side="left", padx=5)

    def show_urgency(self):
        """Display urgency prediction results with a pie chart."""
        (urgency, details), predictions = self.ml_models.predict_urgency()
        self.result_label.config(
            text=f"Urgency Classification:\nPredicted Urgency: {urgency}\n{details}\n\n"
                 "Explanation: This indicates the overall urgency level of complaints. High urgency suggests many complaints need immediate attention."
        )
        explanation = self.ml_models.plot_urgency(self.ax, predictions)
        self.result_label.config(
            text=f"Urgency Classification:\nPredicted Urgency: {urgency}\n{details}\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_clusters(self):
        """Display clustering results with a bar chart."""
        _, explanation, cluster_counts = self.ml_models.cluster_complaints()
        self.result_label.config(
            text=f"Complaint Clusters:\n{explanation}\n\n"
                 "Explanation: Complaints are grouped into clusters based on their descriptions. Each cluster represents a common theme or issue."
        )
        explanation = self.ml_models.plot_clusters(self.ax, cluster_counts)
        self.result_label.config(
            text=f"Complaint Clusters:\n{explanation}\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_resolution_time(self):
        """Display resolution time prediction results with a histogram."""
        time, explanation, predictions = self.ml_models.predict_resolution_time()
        self.result_label.config(
            text=f"Resolution Time Prediction:\n{explanation}\n\n"
                 "Explanation: This predicts the average time to resolve current complaints based on their severity and content."
        )
        explanation = self.ml_models.plot_resolution_time(self.ax, predictions)
        self.result_label.config(
            text=f"Resolution Time Prediction:\n{explanation}\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_sentiment(self):
        """Display sentiment analysis results with a donut chart."""
        sentiments, explanation, sentiment_data = self.ml_models.analyze_sentiment()
        self.result_label.config(
            text=f"Sentiment Analysis:\n{explanation}\n\n"
                 "Explanation: This shows the emotional tone of complaints. A high number of negative sentiments may indicate widespread dissatisfaction."
        )
        explanation = self.ml_models.plot_sentiment(self.ax, sentiment_data)
        self.result_label.config(
            text=f"Sentiment Analysis:\n{explanation}\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_anomalies(self):
        """Display anomaly detection results with a scatter plot."""
        anomaly_ids, explanation, anomaly_labels, severities, complaint_lengths = self.ml_models.detect_anomalies()
        self.result_label.config(
            text=f"Anomaly Detection:\n{explanation}\n\n"
                 "Explanation: Anomalous complaints may have unusual patterns (e.g., high severity, unique descriptions) and might need special attention."
        )
        explanation = self.ml_models.plot_anomalies(self.ax, anomaly_labels, severities, complaint_lengths)
        self.result_label.config(
            text=f"Anomaly Detection:\n{explanation}\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_trends(self):
        """Display complaint trends plot."""
        explanation = self.ml_models.plot_complaint_trends(self.ax)
        self.result_label.config(
            text=f"Complaint Trends Over Time:\n\nExplanation: {explanation}"
        )
        self.canvas.draw()

    def show_categories(self):
        """Display category distribution plot."""
        explanation = self.ml_models.plot_category_distribution(self.ax)
        self.result_label.config(
            text=f"Complaints by Category:\n\nExplanation: {explanation}"
        )
        self.canvas.draw()