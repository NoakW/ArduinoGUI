# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:24:58 2024
@author: noakw
"""

import serial
import time
import customtkinter as ctk
import sys
from functions import validate_inputs
from PIL import Image, ImageTk

cleaning_default = 100
cycle_time = {"entry_value": cleaning_default} # Default cycle time

def start_program(pwm_entry, time_entry, volume_entry, cycle_entry, cycle_time_value, status_label):
    try:
        pwm_value, time_value, volume_value, cycle_value, cycle_time_value = validate_inputs(
            pwm_entry, time_entry, volume_entry, cycle_entry, cycle_time_value
        )

        # Send command
        send_command(f"PROGRAM ({pwm_value}, {time_value}, {volume_value}, "
                     f"{cycle_value}, {cycle_time_value})", status_label)

        # Update status label
        update_status(
            status_label,
            f"Program started with PWM: {pwm_value}, Time: {time_value}, Volume: {volume_value}, "
            f"# \nCleaning cycles: {cycle_value}, Cleaning cycle duration: {cycle_time_value} (s)"
        )
    except ValueError as e:
        update_status(status_label, f"ERROR - {e}")

def send_command(command_list, status_label):
    try:
        print(f"Sending command: {command_list}")
        arduino.write(f"{command_list}\n".encode())  # Write command to Arduino
        update_status(status_label, f"Sent: {command_list}")
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending command: {e}")
        update_status(status_label, "Error sending command")

def on_closing(window, status_label):
    if arduinoConnected:
        try:
            send_command("STOP_MOTOR", status_label)
            send_command("STOP", status_label)

            arduino.close()  # Close the Arduino connection
            print("Serial port closed.")
        except Exception as e:
            print(f"Error closing Arduino connection: {e}")
    window.quit()
    window.destroy()
    sys.exit(0)


def update_status(label, action):
    label.configure(text=f"{action}")


def slider_callback(value, label, entry):
    try:
        entry_value = int(entry.get().strip()) if entry.get().strip().isdigit() else cleaning_default
    except Exception:
        entry_value = cleaning_default
    label.configure(text=f"Number of cleaning cycles: {int(value)}, Cycle duration: {entry_value} (s)")


def update_label_and_store(label, slider, entry):
    entry_value = update_label_from_entry(label, slider, entry)
    cycle_time["entry_value"] = entry_value  # Store the returned value

def update_label_from_entry(label, slider, entry):

    try:
        entry_value = int(entry.get().strip())
    except ValueError:
        entry.delete(0, "end")  # Clear the entry box
        entry_value = cleaning_default  # Default value
        entry.focus()

    if entry_value <= 0:
        entry_value = cleaning_default
        entry.delete(0, "end")

    slider_value = int(slider.get())
    label.configure(
        text=f"Number of cleaning cycles: {slider_value}, Cycle duration: {entry_value} (s)"
    )
    return entry_value


def open_main_window():
    window = ctk.CTk()
    window.geometry("850x450")
    window.title("Process Cycle Control Panel")
    window.resizable(False, False)

    frame_left = ctk.CTkFrame(master=window, width=500, height=400, corner_radius=10)
    frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Attach to the left side

    frame_right = ctk.CTkFrame(master=window, width=500, height=400, corner_radius=10)
    frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Attach to the right side

    actuator_label = ctk.CTkLabel(
        master=frame_left, text="Manual Actuator Control", font=("Arial", 16, "bold"), anchor="center"
    )
    actuator_label.grid(row=0, column=0, padx=10, pady=5)

    divider1 = ctk.CTkFrame(master=frame_left, height=2, fg_color="gray25")
    divider1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    actuator_frame = ctk.CTkFrame(master=frame_left)
    actuator_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    extend_button = ctk.CTkButton(
        master=actuator_frame,
        text="Extend Actuator",
        command=lambda: send_command("EXTEND", status_label),
        fg_color="#4CAF50",
        hover_color="#45A049",
        corner_radius=8,
    )
    extend_button.grid(row=0, column=0, padx=10, pady=5)

    retract_button = ctk.CTkButton(
        master=actuator_frame,
        text="Retract Actuator",
        command=lambda: send_command("RETRACT", status_label),
        fg_color="#FF5722",
        hover_color="#E64A19",
        corner_radius=8,
    )
    retract_button.grid(row=0, column=1, padx=10, pady=5)

    manual_motor_label = ctk.CTkLabel(
        master=frame_left, text="Manual Motor Control", font=("Arial", 16, "bold"), anchor="center"
    )
    manual_motor_label.grid(row=3, column=0, padx=10, pady=5)

    divider2 = ctk.CTkFrame(master=frame_left, height=2, fg_color="gray25")
    divider2.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    manual_entry_frame = ctk.CTkFrame(master=frame_left)
    manual_entry_frame.grid(row=5, column=0, padx=10, pady=10, sticky="n")  # Use grid here instead of pack

    # PWM entry
    pwm_label_manual = ctk.CTkLabel(master=manual_entry_frame, text="PWM: ", font=("Arial", 12), anchor="w")
    pwm_label_manual.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    pwm_entry_manual = ctk.CTkEntry(
        master=manual_entry_frame, placeholder_text="Enter PWM Value (0-255)", width=200
    )
    pwm_entry_manual.grid(row=0, column=1, padx=5, pady=5)
    set_button = ctk.CTkButton(
        master=manual_entry_frame,
        width=50,
        text="Set",
        command=lambda: send_command()
    )
    set_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")




    # Load the image using Pillow
    image = Image.open("logo.png")  # Load the image with Pillow

    logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(230,160))  # Create CTkImage with resized image

    # Add the logo beneath the existing widgets
    logo_label = ctk.CTkLabel(
        master=frame_left, image=logo_image, text="", anchor="center"
    )

    logo_label.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
































    cleaning_label = ctk.CTkLabel(
        master=frame_right, text="CIP Setup", font=("Arial", 16, "bold"), anchor="center"
    )
    cleaning_label.pack(pady=(10, 0))

    divider3 = ctk.CTkFrame(master=frame_right, height=2, fg_color="gray25")
    divider3.pack(pady=10, fill="x", padx=20)

    control_frame_clean = ctk.CTkFrame(master=frame_right)
    control_frame_clean.pack(pady=10, padx=32, fill="x", expand=True)

    entry_frame_right = ctk.CTkFrame(master=control_frame_clean)
    entry_frame_right.grid(row=0, column=0, sticky="n")

    cycle_label = ctk.CTkLabel(master=entry_frame_right, text="Number of Cleaning Cycles: ", font=("Arial", 12),
                               anchor="w")
    cycle_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    cycle_entry = ctk.CTkSlider(
        master=entry_frame_right,
        from_=1,
        to=5,
        command=lambda value: slider_callback(value, cycle_setup_label, cycle_time_entry)
    )
    cycle_entry.set(1)
    cycle_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    cycle_time_label = ctk.CTkLabel(master=entry_frame_right, text="Cleaning Cycle Length: ", font=("Arial", 12),
                                    anchor="w")
    cycle_time_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    cycle_time_entry = ctk.CTkEntry(
        master=entry_frame_right, placeholder_text="Enter Cleaning Duration (s)", width=150
    )
    cycle_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    set_button = ctk.CTkButton(
        master=entry_frame_right,
        width=50,
        text="Set",
        command=lambda: update_label_and_store(cycle_setup_label, cycle_entry, cycle_time_entry)
    )
    set_button.grid(row=1, column=1, padx=0, pady=5, sticky="e")

    cycle_setup_label = ctk.CTkLabel(
        master=entry_frame_right,
        text=f"Number of cleaning cycles: 1, Cycle duration: {cleaning_default} (s)",
        font=("Arial", 12),
        anchor="n"
    )
    cycle_setup_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    status_label = ctk.CTkLabel(
        master=frame_right, text="Status: Ready", font=("Arial", 12), anchor="w"
    )
    status_label.pack(pady=(5, 2), padx=20, fill="x")

    motor_label = ctk.CTkLabel(
        master=frame_right, text="Process Control", font=("Arial", 14, "bold"), anchor="center"
    )
    motor_label.pack(pady=(20, 0))

    divider4 = ctk.CTkFrame(master=frame_right, height=2, fg_color="gray25")
    divider4.pack(pady=10, fill="x", padx=20)

    control_frame_motor = ctk.CTkFrame(master=frame_right)
    control_frame_motor.pack(pady=10, padx=10, fill="x")

    entry_frame = ctk.CTkFrame(master=control_frame_motor)
    entry_frame.grid(row=0, column=0, sticky="n")  # Align to the top

    # PWM entry
    pwm_label = ctk.CTkLabel(master=entry_frame, text="PWM: ", font=("Arial", 12), anchor="w")
    pwm_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    pwm_entry = ctk.CTkEntry(
        master=entry_frame, placeholder_text="Enter PWM Value (0-255)", width=200
    )
    pwm_entry.grid(row=0, column=1, padx=5, pady=5)

    # Time entry
    time_label = ctk.CTkLabel(master=entry_frame, text="Reaction Time: ", font=("Arial", 12), anchor="w")
    time_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    time_entry = ctk.CTkEntry(
        master=entry_frame, placeholder_text="Enter Reaction Time (s)", width=200
    )
    time_entry.grid(row=1, column=1, padx=5, pady=5)

    # Volume entry
    volume_label = ctk.CTkLabel(master=entry_frame, text="Solid Volume: ", font=("Arial", 12), anchor="w")
    volume_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    volume_entry = ctk.CTkEntry(
        master=entry_frame, placeholder_text="Enter Solid Volume (cm^3)", width=200
    )
    volume_entry.grid(row=2, column=1, padx=5, pady=5)

    start_button = ctk.CTkButton(
        master=control_frame_motor,
        text="Start Program",
        width=100,
        height=90,
        fg_color="#4CAF50",
        hover_color="#45A049",
        command=lambda: start_program(pwm_entry, time_entry, volume_entry,
                                      cycle_entry, cycle_time["entry_value"], status_label)
    )

    start_button.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ns")

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, status_label))

    window.mainloop()


arduinoConnected = False

# Appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

try:
    print("Connecting to Arduino")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    print("Connected to Arduino.")
    arduinoConnected = True
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")

open_main_window()

