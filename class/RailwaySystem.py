import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
import os
import sqlite3
from .Booking import Booking
from tkcalendar import Calendar
from collections import OrderedDict
from random import choice
from string import ascii_uppercase, digits

# Declare the database path
db_path = os.path.join(os.path.dirname(
    __file__), "..", "db", "nirctc.db")


class ReservationSystem:
    def book_ticket(self, main_app, current_frame, username):
        # Ticket Booking window
        current_frame.pack_forget()
        book_ticket_window = ctk.CTkFrame(
            main_app, width=320, height=720, corner_radius=10)
        book_ticket_window.pack(fill=tk.BOTH, padx=20, pady=20)

        # PNR code
        pnr_no = ReservationSystem.generate_pnr_no()

        # Connect to database
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Age
        age = ctk.StringVar()
        age_label = ctk.CTkLabel(
            book_ticket_window, text="Enter your age:", font=("Century Gothic Bold", 16))
        age_entry = ctk.CTkEntry(
            book_ticket_window, width=120, height=35, textvariable=age)
        age_label.place(x=40, y=40)
        age_entry.place(x=300, y=40)

        # Full name
        full_name = ctk.StringVar()
        full_name_label = ctk.CTkLabel(
            book_ticket_window, text="Enter your name:", font=("Century Gothic Bold", 16))
        full_name_entry = ctk.CTkEntry(
            book_ticket_window, width=120, height=35, textvariable=full_name)
        full_name_label.place(x=40, y=120)
        full_name_entry.place(x=300, y=120)

        # Keeping a list of all stations
        stations = set()
        for i in cur.execute("select from_station, to_station from train").fetchall():
            stations.add(i[0])
            stations.add(i[1])

        # From station and To station declarations
        from_station = ctk.StringVar(value="Mumbai")
        to_station = ctk.StringVar(value="Mumbai")

        # From Station
        from_station_label = ctk.CTkLabel(
            book_ticket_window, text="Select your boarding station: ", font=("Century Gothic Bold", 16))
        from_station_entry = ctk.CTkComboBox(
            book_ticket_window, values=stations, variable=from_station, width=120, height=40,
            command=lambda v: self.train_select(from_station.get(), to_station.get(), book_ticket_window))
        from_station_label.place(x=40, y=200)
        from_station_entry.place(x=300, y=200)

        # To Station
        to_station_label = ctk.CTkLabel(
            book_ticket_window, text="Select your arriving station: ", font=("Century Gothic Bold", 16))
        to_station_entry = ctk.CTkComboBox(
            book_ticket_window, values=stations, variable=to_station, width=120, height=40,
            command=lambda v: self.train_select(from_station.get(), to_station.get(), book_ticket_window))
        to_station_label.place(x=40, y=280)
        to_station_entry.place(x=300, y=280)

        # Class
        classes = ["SL", "FC", "1A", "2A", "3A", "CC", "3E"]
        class_var = ctk.StringVar(value="SL")
        class_label = ctk.CTkLabel(
            book_ticket_window, text="Select your class: ", font=("Century Gothic Bold", 16))
        class_entry = ctk.CTkComboBox(
            book_ticket_window, values=classes, variable=class_var, width=120, height=40)
        class_label.place(x=450, y=280)
        class_entry.place(x=680, y=280)

        # Date
        calendar_label = ctk.CTkLabel(
            book_ticket_window, text="Select Date of Journey:", font=("Century Gothic Bold", 16))
        calendar = Calendar(book_ticket_window,
                            selectmode='day', year=2023, month=5, day=22)
        calendar_label.place(x=450, y=40)
        calendar.place(x=680, y=40)

        # Add Booking button
        def train_func():
            if ReservationSystem.train and age.get().isdigit():
                return self.add_booking(Booking(pnr_no, username, full_name.get(), age.get(), calendar.get_date(), ReservationSystem.train[0], class_var.get(), from_station.get(), to_station.get()), book_ticket_window, current_frame)

            elif not age.get().isdigit():
                return messagebox.showinfo("Invalid Age!", "Age must be a number!")

            return messagebox.showinfo("No trains!", "There are no trains currently going through the selected stations.")

        add_booking_button = ctk.CTkButton(book_ticket_window, text="Book ticket", width=250, height=50, font=(
            "Century Gothic Bold", 24), command=train_func)
        add_booking_button.place(relx=0.4, rely=0.8)

        # Add Back Button
        back_button = ctk.CTkButton(book_ticket_window, text="Go Back", width=250, height=50, font=(
            "Century Gothic Bold", 24), command=lambda: self.go_back(book_ticket_window, current_frame), fg_color="#FF2400")
        back_button.place(relx=0.7, rely=0.8)

    def cancel_ticket(self, app, current_frame):
        # Remove the current frame
        current_frame.pack_forget()

        # Create the cancel ticket frame
        cancel_ticket_window = ctk.CTkFrame(
            app, width=320, height=720, corner_radius=10)
        cancel_ticket_window.pack(fill=tk.BOTH, padx=20, pady=20)

        # PNR code input
        pnr_var = ctk.StringVar()
        pnr_label = ctk.CTkLabel(cancel_ticket_window, text="Enter the PNR code:", font=(
            "Century Gothic Bold", 16))
        pnr_entry = ctk.CTkEntry(cancel_ticket_window,
                                 textvariable=pnr_var, width=160, height=40)
        pnr_label.place(x=40, y=40)
        pnr_entry.place(x=200, y=40)

        # Cancel button
        cancel_button = ctk.CTkButton(
            cancel_ticket_window, font=(
                "Century Gothic Bold", 16), text="Cancel Ticket", width=200, height=40, command=lambda: self.cancel_booking(pnr_var.get()))
        cancel_button.place(x=400, y=40)

        # Add Back Button
        back_button = ctk.CTkButton(cancel_ticket_window, text="Go Back", width=200, height=40, font=(
            "Century Gothic Bold", 16), command=lambda: self.go_back(cancel_ticket_window, current_frame), fg_color="#FF2400")
        back_button.place(x=640, y=40)

    def go_back(self, current_frame, next_frame):
        current_frame.pack_forget()
        next_frame.pack(fill=tk.BOTH, padx=20, pady=20)

    def check_status(self, app, current_frame):
        # Remove the current frame
        current_frame.pack_forget()

        # Create the status ticket window
        ticket_status_window = ctk.CTkFrame(
            app, width=320, height=720, corner_radius=10)
        ticket_status_window.pack(fill=tk.BOTH, padx=20, pady=20)

        # PNR code input
        pnr_var = ctk.StringVar()
        pnr_label = ctk.CTkLabel(ticket_status_window, text="Enter the PNR code:", font=(
            "Century Gothic Bold", 16))
        pnr_entry = ctk.CTkEntry(ticket_status_window,
                                 textvariable=pnr_var, width=160, height=40)
        pnr_label.place(x=40, y=40)
        pnr_entry.place(x=200, y=40)

        # Status button
        status_button = ctk.CTkButton(
            ticket_status_window, font=(
                "Century Gothic Bold", 16), text="Ticket Status", width=200, height=40, command=lambda: self.booking_status(pnr_var.get(), ticket_status_window))
        status_button.place(x=400, y=40)

        # Add Back Button
        back_button = ctk.CTkButton(ticket_status_window, text="Go Back", width=200, height=40, font=(
            "Century Gothic Bold", 16), command=lambda: self.go_back(ticket_status_window, current_frame), fg_color="#FF2400")
        back_button.place(x=640, y=40)

    @staticmethod
    def generate_pnr_no():
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        characters = ascii_uppercase + digits
        pnr_no = ''.join(choice(characters) for _ in range(6))
        while pnr_no in cur.execute("select pnr_no from bookings").fetchall():
            pnr_no = ''.join(choice(characters) for _ in range(6))
        cur.close()
        con.close()
        return pnr_no

    # Finds an available train with the given boarding and arriving stations
    def train_select(self, from_station, to_station, frame):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        ReservationSystem.train = cur.execute(f"select name from train where from_station='{
                                              from_station}' and to_station='{to_station}'").fetchone()
        if ReservationSystem.train:
            train_text = f"Your train is: {ReservationSystem.train[0]}"
        else:
            train_text = "There are no trains currently going through the selected stations."

        train_label = ctk.CTkLabel(frame, font=(
            "Century Gothic Bold", 16), text=train_text, width=600)
        train_label.place(relx=0.25, y=360)

        cur.close()
        con.close()

    def add_booking(self, booking: Booking, current_frame, next_frame):
        month, day, year = booking.date_of_journey.split("/")
        new_date = f"20{year}-{month}-{day}"
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute(f"INSERT into Booking values ('{booking.pnr_no}', '{booking.name}', '{booking.full_name}', {
                    booking.age}, '{new_date}', '{booking.train}', '{booking.train_class}', '{booking.from_station}', '{booking.to_station}', 'BOOKED')")
        con.commit()
        cur.close()
        con.close()

        messagebox.showinfo("Ticket successfully booked!",
                            "Ticket is successfully booked!")
        current_frame.pack_forget()
        next_frame.pack(fill=tk.BOTH, padx=20, pady=20)

        # Booked history widget
        booked_history_label = ctk.CTkLabel(
            next_frame, font=("Century Gothic Bold", 20), text="Booked Ticket History")
        booked_history_label.place(x=40, y=300)

        booked_history_widget = ctk.CTkFrame(
            next_frame, width=552, height=200, fg_color="#333333")
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
                              booking.name}' ORDER BY date_of_journey DESC LIMIT 10").fetchall()

        for record in records:
            tree.insert("", tk.END, values=record)

        tree.pack(fill="both", expand=True)

        cur.close()
        con.close()

    def cancel_booking(self, pnr_no):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        record = cur.execute(
            f"select * from Booking where pnr_no = '{pnr_no}'").fetchone()
        if record:
            cur.execute(f"delete from Booking where pnr_no = '{pnr_no}'")
            messagebox.showinfo("Ticket successfully cancelled!",
                                "Your ticket is successfully cancelled!")
        else:
            messagebox.showerror("Invalid PNR Code!",
                                 "This is an invalid PNR code!")
        con.commit()
        cur.close()
        con.close()

    def booking_status(self, pnr_no, current_frame):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        record = cur.execute(
            f"select * from Booking where pnr_no = '{pnr_no}'").fetchone()
        if record:
            record = Booking(*record[: -1])
            record_dict = OrderedDict([
                ("Status: ", "BOOKED"),
                ("PNR Code: ", record.pnr_no),
                ("Name: ", record.full_name),
                ("Age: ", record.age),
                ("Train: ", record.train),
                ("Boarding Station: ", record.from_station),
                ("Arriving Station: ", record.to_station),
                ("Class: ", record.train_class),
                ("Date of Journey: ", record.date_of_journey)
            ])

            status_labels = []

            for i in record_dict:
                status_label = ctk.CTkLabel(current_frame, text=i, font=(
                    "Century Gothic Bold", 16))
                record_label = ctk.CTkLabel(current_frame, text=record_dict[i], font=(
                    "Century Gothic Bold", 16))
                status_labels.append((status_label, record_label))

            for i, val in enumerate(status_labels):
                val[0].place(x=40, y=120 + (40 * i))
                val[1].place(x=200, y=120 + (40 * i))
        else:
            messagebox.showerror("Invalid PNR Code!",
                                 "This is an invalid PNR code!")
        con.commit()
        cur.close()
        con.close()
