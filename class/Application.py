import sqlite3
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
from time import strftime
import os
from .RailwaySystem import ReservationSystem
from .User import User

# Declare the database path
db_path = os.path.join(os.path.dirname(
    __file__), "..", "db", "nirctc.db")


class Application:

    # Initialise the main screen
    def __init__(self, app):
        # Make the reservation system
        self.railway = ReservationSystem()
        self.app = app
        self.main_frame = ctk.CTkFrame(app)

        # Welcome title
        welcome_title_label = ctk.CTkLabel(self.main_frame, text="Welcome to NIRCTC", font=(
            "Century Gothic Bold", 32), text_color="#29ab87")
        welcome_title_label.pack(pady=40)

        # Login title
        login_title_label = ctk.CTkLabel(
            self.main_frame, text="Login", font=("Century Gothic Bold", 24))
        login_title_label.pack(padx=10, pady=20)

        # User name input
        user_name_var = tk.StringVar()
        user_name_label = ctk.CTkLabel(
            self.main_frame, text="Enter your username", font=("Century Gothic Bold", 16))
        user_name_entry = ctk.CTkEntry(
            self.main_frame, width=350, height=40, textvariable=user_name_var)
        user_name_label.pack()
        user_name_entry.pack()

        # Password input
        password_var = tk.StringVar()
        password_label = ctk.CTkLabel(
            self.main_frame, text="Enter your password", font=("Century Gothic Bold", 16))
        password_entry = ctk.CTkEntry(
            self.main_frame, width=350, height=40, textvariable=password_var)
        password_label.pack()
        password_entry.pack()

        # Login button
        login_button = ctk.CTkButton(self.main_frame, text="Login", font=(
            "Century Gothic Bold", 16), command=lambda: User(user_name_var.get(), password_var.get()).authenticate(self.app, self.show_user_dashboard), width=250, height=40)
        login_button.pack(pady=40)

        # Register button
        register_button = ctk.CTkButton(self.main_frame, text="Not Registered? Sign up!", font=(
            "Century Gothic Bold", 16), command=lambda: User(user_name_var.get(), password_var.get()).register(), width=250, height=40)
        register_button.pack()

        # Run the app
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        app.mainloop()

    def show_user_dashboard(self, username):
        # Close the login window
        self.main_frame.pack_forget()

        # Dashboard
        dashboard = ctk.CTkFrame(
            self.app, width=320, height=640, corner_radius=10)
        dashboard.pack(fill=tk.BOTH, padx=20, pady=20)

        # Main Image
        image_path = os.path.join(os.path.dirname(
            __file__), "..", "images", "abstract-bg.jpg")
        bg = ctk.CTkImage(dark_image=Image.open(image_path),
                          size=(300, 200))
        background_label = ctk.CTkLabel(
            dashboard, image=bg, text="", corner_radius=10)
        background_label.place(x=30, y=30)

        # Welcome text
        welcome_text = ctk.CTkLabel(dashboard, text=f"Welcome {username}!", font=(
            "Century Gothic Bold", 18))
        welcome_text.place(x=360, y=40)

        # Logout button
        logout_button = ctk.CTkButton(
            dashboard, text="Logout", command=lambda: User.logout(dashboard, self.main_frame), font=(
                "Century Gothic Bold", 16), width=200, height=40, fg_color="#FF2400")
        logout_button.place(x=720, y=30)

        # Separator
        separator = ctk.CTkFrame(
            dashboard, fg_color="#999999", width=560, height=2)
        separator.place(x=360, y=100)

        # Ticket booking button
        ticket_booking_button = ctk.CTkButton(dashboard, text="Book a ticket", command=lambda: self.railway.book_ticket(
            self.app, dashboard, username), font=("Century Gothic Bold", 16), width=160, height=40)
        ticket_booking_button.place(x=360, y=140)

        # Ticket Cancelling button
        ticket_cancelling_button = ctk.CTkButton(dashboard, text="Cancel a ticket", command=lambda: self.railway.cancel_ticket(
            self.app, dashboard), font=("Century Gothic Bold", 16), width=160, height=40, fg_color="#FF2400")
        ticket_cancelling_button.place(x=560, y=140)

        # Ticket Status button
        ticket_status_button = ctk.CTkButton(dashboard, text="Check ticket Status", command=lambda: self.railway.check_status(
            self.app, dashboard), font=("Century Gothic Bold", 16), width=160, height=40, fg_color="#FFBF00")
        ticket_status_button.place(x=760, y=140)

        # Clock widget
        clock_widget = ctk.CTkLabel(
            dashboard, fg_color="#555555", width=560, corner_radius=10, height=80, font=("Century Gothic Bold", 20))
        Application.display_time(clock_widget)
        clock_widget.place(x=360, y=200)

        # Booked history widget
        booked_history_label = ctk.CTkLabel(
            dashboard, font=("Century Gothic Bold", 20), text="Booked Ticket History")
        booked_history_label.place(x=40, y=300)

        booked_history_widget = ctk.CTkFrame(
            dashboard, width=552, height=200, fg_color="#333333")
        booked_history_widget.place(x=360, y=300)
        style = ttk.Style(booked_history_widget)
        style.theme_use("clam")
        style.configure("Treeview", background="#222222",
                        fieldbackground="#222222", foreground="white")

        tree = ttk.Treeview(booked_history_widget, columns=(
            "pnr_no", "date_of_journey", "train", "class", "from_station", "to_station"), show="headings")

        tree.heading("pnr_no", text="PNR No")
        tree.heading("date_of_journey", text="Date of Journey")
        tree.heading("train", text="Train")
        tree.heading("class", text="Class")
        tree.heading("from_station", text="From Station")
        tree.heading("to_station", text="To Station")

        tree.column("pnr_no", width=92)
        tree.column("date_of_journey", width=92)
        tree.column("train", width=104)
        tree.column("class", width=80)
        tree.column("from_station", width=92)
        tree.column("to_station", width=92)

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        records = cur.execute(f"SELECT pnr_no, date_of_journey, train, class, from_station, to_station FROM Booking WHERE user_name='{
                              username}' ORDER BY date_of_journey DESC LIMIT 10").fetchall()

        for record in records:
            tree.insert("", tk.END, values=record)

        tree.pack(fill="both", expand=True)

        cur.close()
        con.close()

    @staticmethod
    def display_time(label):
        string = strftime('%I:%M:%S %p, %d/%m/%Y')
        label.configure(text=string)
        label.after(1000, lambda: Application.display_time(label))
