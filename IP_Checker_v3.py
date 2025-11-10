import ipaddress
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

# Function to get the correct path for bundled resources
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load the CSV file
#df = pd.read_csv(resource_path("Aws_Ranges.csv"))
df = pd.read_csv("Aws_Ranges.csv")

# Create the main window
root = tk.Tk()
root.title("Tetea Cloud-to-Cloud IP Range Checker")
root.geometry("500x400")

# Load and display the banner image
try:
    banner_image = Image.open(resource_path("ca.png"))
    banner_image = banner_image.resize((380, 80), Image.Resampling.LANCZOS)
    banner_photo = ImageTk.PhotoImage(banner_image)
    banner_label = tk.Label(root, image=banner_photo)
    banner_label.image = banner_photo  # Keep a reference
    banner_label.pack(pady=10)
except Exception as e:
    print(f"Banner image could not be loaded: {e}")

# Function to check IP
def check_ip():
    ip_input = ip_entry.get()
    try:
        input_ip = ipaddress.ip_address(ip_input)
        for cidr in df['ip_prefix']:
            if input_ip in ipaddress.ip_network(cidr):
                messagebox.showinfo("Result", f"{ip_input} is within the range {cidr}")
                return
        messagebox.showinfo("Result", f"{ip_input} does NOT match any range.")
    except ValueError:
        messagebox.showerror("Error", "Invalid IP address format.")

# UI Elements
tk.Label(root, text="Enter IP Address:").pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.pack()

tk.Button(root, text="Check", command=check_ip).pack(pady=20)

# Run the app
root.mainloop()