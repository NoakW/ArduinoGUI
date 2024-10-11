# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 09:42:54 2024

@author: noakw
"""

import serial
import time
import customtkinter

# Function to send command to Arduino
# Set appearance and theme
customtkinter.set_appearance_mode("dark")  # Mode
customtkinter.set_default_color_theme("dark-blue")  # Theme

rpm_max = 315

arduinoConnected = False;
try:
    # Open the serial connection to Arduino, adjust COM port if needed)
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1) 
    print("Connected to Arduino.")
    arduinoConnected = True;
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    
def rpm_conv(value):
    approx_rpm = int(rpm_max * value)
    if approx_rpm <= 50:
        approx_rpm = 0
    return approx_rpm
    
def slider_callback(value):
    approx_rpm = rpm_conv(value)
    pwm_value = int(value * 255)  # Scale to 0-255 for PWM
    send_command(f"SET_PWM {pwm_value}")
    status_label.configure(text=f"RPM: {int(approx_rpm)}")# Send PWM command to Arduino

def slider_callback2(value):
    deg_value = int(180*value)
    send_command(f"SET_SERVO {deg_value}")
    
def send_command(command):
    try:
        print(f"Sending command: {command}")
        arduino.write(f"{command}\n".encode())  # Send command to Arduino
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending command: {e}")

# Function to handle window closing
def on_closing(arduinoConnected):
    if arduinoConnected:
        send_command("SET_PWM 0")#
        arduino.close()  # Close the serial connection
        print("Serial port closed.")
    window.destroy() #Close the Tkinter window
         
    

# Create the main window
window = customtkinter.CTk()
window.geometry("600x550")

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

rpm_slider = customtkinter.CTkSlider(master=frame, command=slider_callback, from_=0, to=1)
rpm_slider.pack(pady=40, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame,placeholder_text="Enter RPM")
entry_1.pack(pady=12,padx=10)

slider2 = customtkinter.CTkSlider(master=frame, command=slider_callback2, from_=0, to=1)
slider2.pack(pady=40, padx=10)

status_label = customtkinter.CTkLabel(master=frame, text="Current RPM: 0")
status_label.pack(pady=12, padx=10)

# Code for closing window
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(arduinoConnected))
window.mainloop()






