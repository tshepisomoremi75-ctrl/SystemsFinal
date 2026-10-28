import tkinter as tk
from tkinter import messagebox
import sqlite3

from bookings import Booking, get_lecturer_bookings, cancel_booking


class LecturerDashboard:

    def __init__(self, root, fullname, campus):

        self.root = root
        self.fullname = fullname
        self.campus = campus

        self.window = tk.Toplevel(root)
        self.window.title("Lecturer Dashboard")
        self.window.geometry("800x600")

        # Heading
        tk.Label(
            self.window,
            text="SMART CAMPUS RESOURCE BOOKING SYSTEM",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(
            self.window,
            text=f"Welcome: {self.fullname}",
            font=("Arial", 12)
        ).pack()

        tk.Label(
            self.window,
            text=f"Campus: {self.campus}",
            fg="blue"
        ).pack(pady=5)

        # Buttons
        tk.Button(
            self.window,
            text="View Resources / Availability",
            width=35,
            bg="navy",
            fg="white",
            command=self.view_resources
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Create Booking",
            width=35,
            bg="green",
            fg="white",
            command=self.create_booking
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="My Bookings / Cancel",
            width=35,
            bg="orange",
            fg="white",
            command=self.my_bookings
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Refresh",
            width=35,
            bg="purple",
            fg="white",
            command=self.refresh
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Log Out",
            width=35,
            bg="red",
            fg="white",
            command=self.logout
        ).pack(pady=5)

    # ========================================
    # VIEW RESOURCES
    # ========================================

    def view_resources(self):

        try:

            conn = sqlite3.connect("database/campus.db")
            cursor = conn.cursor()

            cursor.execute("""
            SELECT id,
                   resource_code,
                   resource_name,
                   resource_type,
                   campus,
                   availability
            FROM resources
            WHERE campus = ?
            """, (self.campus,))

            resources = cursor.fetchall()

            conn.close()

            resource_window = tk.Toplevel(self.window)
            resource_window.title("Resources / Availability")
            resource_window.geometry("700x500")

            text_box = tk.Text(
                resource_window,
                width=90,
                height=25
            )

            text_box.pack(pady=10)

            if not resources:

                text_box.insert(
                    tk.END,
                    "No resources available."
                )
                return

            for row in resources:

                text_box.insert(
                    tk.END,
                    f"\nID: {row[0]}\n"
                    f"Resource Code: {row[1]}\n"
                    f"Resource Name: {row[2]}\n"
                    f"Resource Type: {row[3]}\n"
                    f"Campus: {row[4]}\n"
                    f"Availability: {row[5]}\n"
                    f"{'-' * 50}\n"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================
    # CREATE BOOKING
    # ========================================

    def create_booking(self):

        booking_window = tk.Toplevel(self.window)
        booking_window.title("Create Booking")
        booking_window.geometry("450x400")

        tk.Label(
            booking_window,
            text="Resource Code"
        ).pack()

        resource_code = tk.Entry(
            booking_window,
            width=30
        )
        resource_code.pack(pady=5)

        tk.Label(
            booking_window,
            text="Booking Date (YYYY-MM-DD)"
        ).pack()

        booking_date = tk.Entry(
            booking_window,
            width=30
        )
        booking_date.pack(pady=5)

        tk.Label(
            booking_window,
            text="Start Time (HH:MM)"
        ).pack()

        start_time = tk.Entry(
            booking_window,
            width=30
        )
        start_time.pack(pady=5)

        tk.Label(
            booking_window,
            text="Duration (Hours)"
        ).pack()

        duration = tk.Entry(
            booking_window,
            width=30
        )
        duration.pack(pady=5)

        def save_booking():

            try:

                booking = Booking(
                    self.fullname,
                    resource_code.get(),
                    booking_date.get(),
                    start_time.get(),
                    int(duration.get()),
                    self.campus
                )

                if booking.save():

                    messagebox.showinfo(
                        "Success",
                        "Booking Created Successfully"
                    )

                    booking_window.destroy()

                else:

                    messagebox.showerror(
                        "Error",
                        "Booking already exists"
                    )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

        tk.Button(
            booking_window,
            text="Save Booking",
            bg="green",
            fg="white",
            command=save_booking
        ).pack(pady=15)

    # ========================================
    # MY BOOKINGS
    # ========================================

    def my_bookings(self):

        bookings = get_lecturer_bookings(
            self.fullname
        )

        booking_window = tk.Toplevel(self.window)
        booking_window.title("My Bookings")
        booking_window.geometry("700x500")

        text_box = tk.Text(
            booking_window,
            width=80,
            height=20
        )

        text_box.pack(pady=10)

        if not bookings:

            text_box.insert(
                tk.END,
                "No bookings found."
            )

        else:

            for booking in bookings:

                text_box.insert(
                    tk.END,
                    f"\nBooking ID: {booking[0]}\n"
                    f"Resource Code: {booking[2]}\n"
                    f"Booking Date: {booking[3]}\n"
                    f"Start Time: {booking[4]}\n"
                    f"Duration: {booking[5]} Hours\n"
                    f"Campus: {booking[6]}\n"
                    f"{'-' * 40}\n"
                )

        tk.Label(
            booking_window,
            text="Enter Booking ID To Cancel"
        ).pack()

        booking_id = tk.Entry(
            booking_window,
            width=20
        )
        booking_id.pack(pady=5)

        def do_cancel():

            try:

                cancel_booking(
                    int(booking_id.get())
                )

                messagebox.showinfo(
                    "Success",
                    "Booking Cancelled Successfully"
                )

                booking_window.destroy()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

        tk.Button(
            booking_window,
            text="Cancel Booking",
            bg="red",
            fg="white",
            command=do_cancel
        ).pack(pady=10)

    # ========================================
    # REFRESH
    # ========================================

    def refresh(self):

        messagebox.showinfo(
            "Refresh",
            "Dashboard Refreshed"
        )

    # ========================================
    # LOG OUT
    # ========================================

    def logout(self):

        self.window.destroy()
        self.root.deiconify()