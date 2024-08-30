import sqlite3
import os
from tkinter import messagebox
import tkinter as tk

# Declare the database path
db_path = os.path.join(os.path.dirname(
    __file__), "..", "db", "nirctc.db")


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, current_frame, next_frame):
        # Connect to database
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Empty fields
        if self.username == "" or self.password == "":
            messagebox.showerror(
                "Error", "All fields are required", parent=current_frame)
            return

        # Find the authenticated username
        logged_name = cur.execute(
            f"select * from logged_users where username='{self.username}'").fetchone()

        # If the name is present
        if logged_name:

            # If password is correct, go to dashboard
            if logged_name[1] == self.password:
                next_frame(self.username)
            else:
                messagebox.showerror(
                    "Error", "Incorrect password", parent=current_frame)
        else:
            messagebox.showerror(
                "Error", "Username doesn't exist", parent=current_frame)

        # Close the database
        cur.close()
        con.close()

    def register(self):
        # Connect to database
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Empty fields
        if self.username == "" or self.password == "":
            messagebox.showerror(
                "Error", "All fields are required", parent=self.app)
            return

        # Insert the new user details
        cur.execute(
            f"insert into logged_users values ('{self.username}', '{self.password}')")
        con.commit()

        # Alert successful registration
        messagebox.showinfo(
            "You're in!", "You're registered! Now try logging in.")

        # Close the database
        cur.close()
        con.close()

    @staticmethod
    def logout(current_frame, next_frame):
        current_frame.pack_forget()
        next_frame.pack(fill=tk.BOTH, expand=True)
