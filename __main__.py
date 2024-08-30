import customtkinter as ctk
from classes.Application import Application
import sqlite3
import os

"""
Database: NIRCTC

Table: User
    username TEXT
    password TEXT

Table: Booking
    pnr_no TEXT PRIMARY KEY
    user_name TEXT
    full_name TEXT
    age INT
    date_of_journey DATE
    Class TEXT
    from_station TEXT
    to_station TEXT

Table: Train
    name TEXT
    from_station TEXT
    to_station TEXT
    no_of_seats INT
"""

"""
train_data = [
    ("Rajdhani Express", "New Delhi", "Mumbai", 300),
    ("Shatabdi Express", "Chennai", "Bangalore", 250),
    ("Duronto Express", "Howrah", "Pune", 200),
    ("Gatimaan Express", "Delhi", "Agra", 150),
    ("Humsafar Express", "Jammu", "Trivandrum", 180),
    ("Deccan Queen", "Mumbai", "Pune", 220),
    ("Lucknow Mail", "Lucknow", "New Delhi", 280),
    ("Chennai Express", "Chennai", "New Delhi", 320),
    ("Mysore Express", "Mysore", "Bangalore", 180),
    ("Golden Temple Mail", "Amritsar", "Mumbai", 200),
    ("Kolkata Mail", "Howrah", "Mumbai", 260),
    ("Goa Express", "Mumbai", "Madgaon", 150),
    ("Karnataka Express", "New Delhi", "Bangalore", 280),
    ("Ahmedabad Express", "Ahmedabad", "Mumbai", 200),
    ("Kashi Vishwanath Express", "Varanasi", "New Delhi", 220),
    ("Bhopal Express", "Bhopal", "New Delhi", 180),
    ("Raptisagar Express", "Ernakulam", "Amritsar", 240),
    ("Malwa Express", "Indore", "Jammu", 200),
    ("Purushottam Express", "Puri", "New Delhi", 300),
    ("Sampark Kranti Express", "Bandra", "Delhi", 250),
    ("Sunrise Express", "Jaipur", "Udaipur", 180),
    ("Mountain Explorer", "Shimla", "Manali", 220),
    ("Coastal Voyager", "Kochi", "Goa", 200),
    ("Silk Route Express", "Kolkata", "Guwahati", 250),
    ("Desert Mirage", "Jaisalmer", "Bikaner", 160),
    ("Royal Bengal Express", "Howrah", "Siliguri", 230),
    ("City of Lakes", "Udaipur", "Bhopal", 210),
    ("Eternal Sands Express", "Jodhpur", "Pushkar", 190),
    ("Green Valley Express", "Darjeeling", "Gangtok", 180),
    ("Western Ghats Explorer", "Mangalore", "Kozhikode", 240),
    ("Golden Sands Express", "Puri", "Vizag", 200),
    ("Northern Lights Express", "Amritsar", "Shimla", 220),
    ("Southern Charm Express", "Chennai", "Kanyakumari", 260),
    ("Majestic Himalayan", "Dehradun", "Nainital", 180),
    ("Eastern Delight", "Howrah", "Patna", 200),
    ("Heart of India", "Bhopal", "Khajuraho", 190),
    ("Mystic Mysuru", "Mysore", "Ooty", 220),
    ("Sunset Serenity", "Kochi", "Kovalam", 210),
    ("Coastal Paradise", "Goa", "Mangalore", 230),
    ("Royal Rajasthan", "Jaipur", "Jodhpur", 240),
]
"""

# Set appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Main application GUI
app = ctk.CTk()
app.geometry("1024x600")
app.title("NIRCTC")
railway_system = Application(app)
