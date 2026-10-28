import tkinter as tk
from tkinter import messagebox


class OperatorDashboard:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        tk.Label(
            self.window,
            text="System Operator",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Campus Reports"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Compare Campuses"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Statistics"
        ).pack(pady=5)