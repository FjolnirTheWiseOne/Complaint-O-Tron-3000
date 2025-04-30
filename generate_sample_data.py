import random
import numpy as np
from datetime import date, timedelta
import bcrypt
import json

# Lists for generating realistic data
first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Karen", "Leo", "Mia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Lee", "Wilson", "Anderson", "Taylor", "Thomas"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"]

# Templates for complaint descriptions
templates = {
    "Service": [
        "The service was {adjective}. The staff was {adjective}.",
        "I am {emotion} with the service I received."
    ],
    "Product": [
        "The product I received was {adjective}. It did not meet my expectations.",
        "There is a problem with the product: {issue}."
    ],
    "Billing": [
        "There is an error in my bill. I was charged ${amount} incorrectly.",
        "I am {emotion} about the billing issue."
    ],
    "Other": [
        "I have a complaint about {topic}. It was {adjective}."
    ]
}

adjectives = ["terrible", "poor", "bad", "unsatisfactory", "disappointing", "frustrating"]
emotions = ["disappointed", "frustrated", "angry", "unhappy"]
issues = ["defective", "broken", "not as described", "late"]
topics = ["delivery", "website", "customer support", "other"]

# Functions
def generate_user(id):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f"{first_name} {last_name}"
    age = max(18, min(80, round(np.random.normal(40, 10))))
    gender = random.choices(["Male", "Female", "Other"], weights=[0.6, 0.35, 0.05])[0]
    location = random.choices(cities, weights=[0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])[0]
    username = (first_name[0] + last_name).lower()
    password = "password123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    phone = f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"
    return {
        "username": username,
        "password": hashed_password,
        "email": email,
        "phone": phone,
        "name": name,
        "age": age,
        "gender": gender,
        "location": location
    }

def generate_description(category):
    template = random.choice(templates[category])
    description = template.format(
        adjective=random.choice(adjectives),
        emotion=random.choice(emotions),
        issue=random.choice(issues),
        amount=str(random.randint(10,100)),
        topic=random.choice(topics)
    )
    return description

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Generate users, including the moderator account
num_users = 15
users = [generate_user(i) for i in range(1, num_users + 1)]

# Add the moderator account 'mod1'
mod_password = "modpass1".encode('utf-8')
mod_hashed_password = bcrypt.hashpw(mod_password, bcrypt.gensalt()).decode('utf-8')
mod_user = {
    "username": "mod1",
    "password": mod_hashed_password,
    "email": "mod1@example.com",
    "phone": "123-456-7890"
}
users.append(mod_user)

# Generate complaints
num_complaints = 35
complaints = []
usernames = [user["username"] for user in users]
weights = [5, 4, 3, 2, 1] + [1] * (num_users - 5) + [2]  # Adjust weights for mod1
start_date = date(2023, 1, 1)
end_date = date.today()

for i in range(1, num_complaints + 1):
    username = random.choices(usernames, weights=weights)[0]
    category = random.choices(["Service", "Product", "Billing", "Other"], weights=[0.4, 0.3, 0.2, 0.1])[0]
    severity = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.15, 0.25, 0.3, 0.2])[0]
    description = generate_description(category)
    status = "Open"
    date_str = random_date(start_date, end_date).strftime("%Y-%m-%d")
    complaint = {
        "id": i,
        "username": username,
        "category": category,
        "severity": severity,
        "description": description,
        "status": status,
        "date": date_str
    }
    complaints.append(complaint)

# Save to files
with open("users.json", "w") as f:
    json.dump(users, f, indent=4)

with open("complaints.json", "w") as f:
    json.dump(complaints, f, indent=4)

print("Sample data generated and saved to users.json and complaints.json")