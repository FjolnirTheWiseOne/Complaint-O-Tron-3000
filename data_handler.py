import json
import os
import sys
from datetime import datetime
import bcrypt
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DataHandler:
    def __init__(self):
        """Initialize the DataHandler with paths to user and complaint data files."""
        # Determine the base directory (where the .exe is located)
        self.base_dir = self.get_base_dir()
        self.users_file = os.path.join(self.base_dir, "users.json")
        self.complaints_file = os.path.join(self.base_dir, "complaints.json")
        self.complaints_csv_file = os.path.join(self.base_dir, "complaints.csv")
        self.load_data()

    def get_base_dir(self):
        """Get the base directory of the application (where the .exe is located)."""
        if getattr(sys, 'frozen', False):
            # If running as a PyInstaller .exe, use the directory of the .exe
            return os.path.dirname(sys.executable)
        else:
            # If running as a Python script, use the script's directory
            return os.path.dirname(os.path.abspath(__file__))

    def load_data(self):
        """Load user and complaint data from JSON files, or initialize with default data."""
        # Load or initialize users
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON in {self.users_file}. Initializing users as empty list.")
                self.users = []
        else:
            # Initialize with a default moderator account
            default_password = "modpass1".encode('utf-8')
            hashed_password = bcrypt.hashpw(default_password, bcrypt.gensalt()).decode('utf-8')
            self.users = [
                {"username": "mod1", "password": hashed_password, "email": "mod1@example.com", "phone": "123-456-7890"}
            ]

        # Load or initialize complaints
        if os.path.exists(self.complaints_file):
            try:
                with open(self.complaints_file, 'r') as f:
                    self.complaints = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON in {self.complaints_file}. Initializing complaints as empty list.")
                self.complaints = []
        else:
            self.complaints = []

        # Validate and fix invalid password hashes for users
        for user in self.users:
            if not self.is_valid_bcrypt_hash(user['password']):
                logging.warning(f"Invalid password hash for user {user['username']}. Regenerating hash.")
                default_password = "modpass1" if user['username'] == "mod1" else "defaultpass"
                user['password'] = self.hash_password(default_password)

        # Save both users and complaints to their respective files
        self.save_data()

    def is_valid_bcrypt_hash(self, hashed_password):
        """Check if the hashed password is a valid bcrypt hash."""
        try:
            if not isinstance(hashed_password, str) or not hashed_password.startswith('$2b$'):
                return False
            bcrypt.checkpw(b"test", hashed_password.encode('utf-8'))
            return True
        except (ValueError, TypeError):
            return False

    def hash_password(self, password):
        """Hash a password using bcrypt."""
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        return hashed

    def save_data(self):
        """Save user and complaint data to JSON files and CSV."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.complaints_file, 'w') as f:
            json.dump(self.complaints, f, indent=4)
        # Save complaints to CSV as well
        self.save_complaints_to_csv()

    def save_complaints_to_csv(self):
        """Save all complaints to a CSV file."""
        try:
            df = pd.DataFrame(self.complaints)
            if not df.empty:
                df.to_csv(self.complaints_csv_file, index=False)
            else:
                # If there are no complaints, create an empty CSV with the correct headers
                pd.DataFrame(columns=["id", "username", "category", "severity", "description", "status", "date"]).to_csv(self.complaints_csv_file, index=False)
            logging.info(f"Successfully saved complaints to {self.complaints_csv_file}")
        except Exception as e:
            logging.error(f"Error saving complaints to CSV: {str(e)}", exc_info=True)

    def authenticate_user(self, username, password):
        """Authenticate a user by checking their username and password."""
        try:
            input_password = password.encode('utf-8')
            for user in self.users:
                if user['username'] == username:
                    stored_password = user['password']
                    if not self.is_valid_bcrypt_hash(stored_password):
                        logging.error(f"Invalid password hash for user {username}")
                        return None
                    if bcrypt.checkpw(input_password, stored_password.encode('utf-8')):
                        return user
                    else:
                        return None
            return None
        except Exception as e:
            logging.error(f"Error in authenticate_user for {username}: {str(e)}", exc_info=True)
            return None

    def register_user(self, username, password, email, phone):
        """Register a new user with hashed password and contact info."""
        hashed_password = self.hash_password(password)
        new_user = {
            "username": username,
            "password": hashed_password,
            "email": email,
            "phone": phone
        }
        self.users.append(new_user)
        self.save_data()
        logging.info(f"Registered new user: {username}")

    def get_user_data(self):
        """Return the list of all users."""
        return self.users

    def update_user_info(self, username, new_email=None, new_phone=None, new_password=None):
        """Update user information such as email, phone, and password."""
        for user in self.users:
            if user['username'] == username:
                if new_email:
                    user['email'] = new_email
                if new_phone:
                    user['phone'] = new_phone
                if new_password:
                    user['password'] = self.hash_password(new_password)
                self.save_data()
                logging.info(f"Updated user info for {username}")
                return user
        logging.error(f"User not found: {username}")
        raise ValueError("User not found")

    def add_complaint(self, username, category, severity, description):
        """Add a new complaint with the current date."""
        complaint = {
            "id": len(self.complaints) + 1,
            "username": username,
            "category": category,
            "severity": severity,
            "description": description,
            "status": "Open",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.complaints.append(complaint)
        self.save_data()
        logging.info(f"Added complaint ID {complaint['id']} for user {username}")

    def get_user_complaints(self, username):
        """Get all complaints for a specific user."""
        return [complaint for complaint in self.complaints if complaint['username'] == username]

    def get_all_complaints(self):
        """Get all complaints in the system."""
        return self.complaints

    def update_complaint_status(self, complaint_id, new_status):
        """Update the status of a complaint."""
        for complaint in self.complaints:
            if complaint['id'] == complaint_id:
                complaint['status'] = new_status
                self.save_data()
                logging.info(f"Updated status of complaint ID {complaint_id} to {new_status}")
                return
        logging.error(f"Complaint not found: ID {complaint_id}")
        raise ValueError("Complaint not found")