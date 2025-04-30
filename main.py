import tkinter as tk
from ui import WelcomeScreen, LoginScreen, HomeScreen, ModeratorScreen
from data_handler import DataHandler
from ml_models import MLModels
import sys

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Complaint-O-Tron 3000")
        self.root.geometry("800x600")
        self.data_handler = DataHandler()
        self.ml_models = MLModels(self.data_handler)

        # Bind the window close event to a cleanup function
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start with the welcome screen
        self.current_screen = None
        self.show_welcome_screen()

    def show_welcome_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = WelcomeScreen(self.root, self.show_login_screen)

    def show_login_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = LoginScreen(self.root, self.handle_login, self.data_handler)

    def handle_login(self, username, password):
        user = self.data_handler.authenticate_user(username, password)
        if user:
            if username == "mod1":  # Assuming mod1 is the moderator
                self.show_moderator_screen()
            else:
                self.show_home_screen(user)
        else:
            tk.messagebox.showerror("Error", "Invalid username or password", parent=self.root)

    def show_home_screen(self, user):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = HomeScreen(self.root, user, self.data_handler, self.show_login_screen)

    def show_moderator_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = ModeratorScreen(self.root, self.data_handler, self.ml_models, self.show_login_screen)

    def on_closing(self):
        """Handle the window close event by saving data and exiting the application."""
        # Save all data before closing
        self.data_handler.save_data()
        # Destroy the root window
        self.root.destroy()
        # Exit the Python process to terminate the PyCharm run session
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()