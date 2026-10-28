import tkinter as tk
from tkinter import messagebox


class AdminDashboard:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        tk.Label(
            self.window,
            text="Campus Administrator",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Add Resource"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="View Resources"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="View Bookings"
        ).pack(pady=5)