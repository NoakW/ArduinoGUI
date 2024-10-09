# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 09:42:54 2024

@author: noakw
"""

import serial
import time
import customtkinter

# Function to send command to Arduino
def send_command(command):
    try:
        print(f"Sending command: {command}")
        arduino.write(f"{command}\n".encode())  # Send command to Arduino
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending command: {e}")

# Function to handle window closing
def on_closing():
    arduino.close()  # Close the serial connection
    print("Serial port closed.")
    window.destroy()  # Close the Tkinter window
    
def slider_callback(value):
    progressbar_1.set(value)
    

# Set appearance and theme
customtkinter.set_appearance_mode("dark")  # Mode
customtkinter.set_default_color_theme("dark-blue")  # Theme
# Open the serial connection to Arduino, adjust COM port if needed)
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    print("Connected to Arduino.")
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")

# Create the main window
window = customtkinter.CTk()
window.geometry("500x350")

# Create a frame for content
frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Buttons to send commands to the Arduino
btn_on_blue = customtkinter.CTkButton(master=frame, text="Turn ON Blue LED", command=lambda: send_command("HIGH_BLUE"))
btn_on_blue.pack(pady=10)

btn_off_blue = customtkinter.CTkButton(master=frame, text="Turn OFF Blue LED", command=lambda: send_command("LOW_BLUE"))
btn_off_blue.pack(pady=10)

btn_on_red = customtkinter.CTkButton(master=frame, text="Turn ON Red LED", command=lambda: send_command("HIGH_RED"))
btn_on_red.pack(pady=10)

btn_off_red = customtkinter.CTkButton(master=frame, text="Turn OFF Red LED", command=lambda: send_command("LOW_RED"))
btn_off_red.pack(pady=10)

progressbar_1 = customtkinter.CTkProgressBar(master=window)
progressbar_1.pack(pady=12,padx=10)
rpm_slider = customtkinter.CTkSlider(master=window,command=slider_callback,from_=0,to=1)
rpm_slider.pack(pady=12,padx=10)

entry_1 = customtkinter.CTkEntry(master=frame,placeholder_text="HELLO")
entry_1.pack(pady=12,padx=10)

party_btn = customtkinter.CTkButton(master=frame, text="Party",command=lambda: send_command("PARTY"))
party_btn.pack(pady=10)

# Code for closing window
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()

# Detach arduino from prot
arduino.close()
