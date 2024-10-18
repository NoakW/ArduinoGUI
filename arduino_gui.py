import serial
import time
import customtkinter
import sys

# Global variables
rpm_max = 315
arduinoConnected = False
opt_menu = None
status_label = None
remembered = False
pwm_1 = 255
reverse = 1

# Set appearance and theme
customtkinter.set_appearance_mode("dark")  # Mode
customtkinter.set_default_color_theme("green")  # Theme

try:
    print("Connecting to Arduino")
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    print("Connected to Arduino.")
    arduinoConnected = True
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")

# Functions
def rpm_conv(value):
    approx_rpm = int(rpm_max * value)
    if approx_rpm < 50:
        approx_rpm = 0
    return approx_rpm

def slider_callback(value, motorID):
        approx_rpm = rpm_conv(value)
        pwm_value = int(value * 255)
        send_command(f"SET_PWM_{motorID} {pwm_value}")
        status_label.configure(text=f"RPM: {approx_rpm}")
    
def send_command(command):
    try:
        print(f"Sending command: {command}")
        arduino.write(f"{command}\n".encode())  # Send command to Arduino
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending command: {e}")

def on_closing(window):
    if arduinoConnected:
        try:
            send_command("SET_PWM_1 0")
            send_command("SET_PWM_2 0")# Stop the motor
            arduino.close()  # Close the Arduino connection
            print("Serial port closed.")
        except Exception as e:
            print(f"Error closing Arduino connection: {e}")
    window.quit()
    window.destroy()
    sys.exit(0)

def on_closing_sub(window):
    window.quit()
    window.destroy() 
    
    
def start_motor(pwm_entry,reverse_checkbox,motorID):
    # Get the PWM value from the entry
    pwm_value = pwm_entry.get().strip()  # Remove any surrounding whitespace
    
    # Default to 255 if the entry is empty
    if not pwm_value:
        pwm_value = 255
    else:
        # Try to convert to an integer and validate
        try:
            pwm_value = int(pwm_value)
            if pwm_value < 0 or pwm_value > 255:
                raise ValueError  # Raise error if out of range
        except ValueError:
            print("Error: Invalid input. Please enter a number between 0 and 255.")
            return
    
    # Adjust PWM value if reversing direction
    if reverse_checkbox.get():
        pwm_value = -pwm_value  # Reverse the value if checked
    send_command(f"SET_PWM_{motorID} {pwm_value}")

    
def run_config(motorID):
    config_window = customtkinter.CTk()
    config_window.geometry("300x250")
    config_window.title("Set RPM")

    # Frame setup
    configframe = customtkinter.CTkFrame(master=config_window)
    configframe.pack(pady=20, padx=60, fill="both", expand=True)

    # Add a label for PWM entry
    pwm_label = customtkinter.CTkLabel(master=configframe, text="Enter PWM Value (0-255):")
    pwm_label.pack(pady=10)
    
    # Add text entry box for PWM input
    pwm_entry = customtkinter.CTkEntry(master=configframe, placeholder_text="PWM Value")
    pwm_entry.pack(pady=10)
    
    reverse_checkbox = customtkinter.CTkCheckBox(master=configframe, text="Reverse direction")
    reverse_checkbox.pack(pady=10)
    
    # Add a start button to send the PWM value
    startbutton = customtkinter.CTkButton(master=configframe, text="Start", command=lambda: start_motor(pwm_entry,reverse_checkbox,motorID))
    startbutton.pack(pady=10)

    # Close protocol
    config_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_sub(config_window))
    config_window.mainloop()
    
# Verify login credentials
def verify_login(entry_username, entry_password, login_win, whitelist_file):
    username = entry_username.get()
    password = entry_password.get()

    # Read the whitelist file
    try:
        with open(whitelist_file, 'r') as file:
            whitelist = file.readlines()

        # Check if username and password match any entry
        for entry in whitelist:
            entry_user, entry_pass = entry.strip().split(",")
            if username == entry_user and password == entry_pass:
                print("Access granted")
                login_win.destroy()  # Close login window
                open_main_window()   # Open main control window
                return
            
        print("Wrong")

    except Exception as e:
        print(f"Error reading whitelist: {e}")
        
        
def login_guest(entry_username, entry_password, login_win, whitelist_file):
    # Read the whitelist file
    try:
        with open(whitelist_file, 'r') as file:
            whitelist = file.readlines()

        # Check if username and password match any entry
        for entry in whitelist:
            entry_user, entry_pass = entry.strip().split(",")
            if entry_username == entry_user and entry_password == entry_pass:
                print("Access granted")
                login_win.destroy()  # Close login window
                open_main_window()   # Open main control window
                return
            
        print("Wrong")

    except Exception as e:
        print(f"Error reading whitelist: {e}")
    
# Main motor/servo control window
def open_main_window():
    global opt_menu, status_label, pwm_1
    # GUI setup
    window = customtkinter.CTk()
    window.geometry("600x550")
    window.title("Motor and Servo Controller")

    # Frame setup
    frame = customtkinter.CTkFrame(master=window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    # Slider for motor/servo control
    slider_1 = customtkinter.CTkSlider(master=frame, from_=-1, to=1, command=lambda value: slider_callback(value, motorID=1))
    slider_1.pack(pady=20, padx=10)
    

    slider_2 = customtkinter.CTkSlider(master=frame, from_=-1, to=1, command=lambda value: slider_callback(value, motorID=2))
    slider_2.pack(pady=20, padx=10)
    # Slider status label
    status_label = customtkinter.CTkLabel(master=frame, text="Current RPM: 0")
    status_label.pack(pady=10)

    startbutton = customtkinter.CTkButton(master=frame, text="Default run", command=lambda: send_command(f"SET_PWM_1 {pwm_1}"))
    startbutton.pack(pady=10)
        
    program_1 = customtkinter.CTkButton(master=frame, text="Options", command=lambda: run_config(1))   # Window close protocol
    program_1.pack(pady=10)
    
    cleanbutton = customtkinter.CTkButton(master=frame, text="Default run", command=lambda: send_command(f"SET_PWM_1 {pwm_1}"))
    cleanbutton.pack(pady=10)
        
    program_2 = customtkinter.CTkButton(master=frame, text="Options", command=lambda: run_config(1))   # Window close protocol
    program_2.pack(pady=10)
    
    
    
    
    
    
    
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

    # Run main loop
    window.mainloop()

# Login window function
def open_login_window():
    # Creating login window
    login_win = customtkinter.CTk()  # Initialize login window
    login_win.geometry("300x350")
    login_win.title("Group 8 Industries - Login")

    # Username entry
    entry_username = customtkinter.CTkEntry(master=login_win, placeholder_text="Enter Username")
    entry_username.pack(pady=10)

    # Password entry
    entry_password = customtkinter.CTkEntry(master=login_win, placeholder_text="Enter Password", show="*")
    entry_password.pack(pady=10)

    # Error label
    label_error = customtkinter.CTkLabel(master=login_win, text="")
    label_error.pack()

    remember_me = customtkinter.CTkCheckBox(master=login_win, text="Remember Me")
    remember_me.pack()
    # Login button
    filepath = "arduino_whitelist.txt"
    login_button = customtkinter.CTkButton(master=login_win, text="Login",
                                           command=lambda: verify_login(entry_username, entry_password, login_win,filepath))
    login_button.pack(pady=20)
    
    login_guest_button = customtkinter.CTkButton(master=login_win, text="Login as guest",
                                           command=lambda: login_guest("guest", "admin", login_win,filepath))
    login_guest_button.pack(pady=20)
    
    login_win.protocol("WM_DELETE_WINDOW", lambda: on_closing(login_win))    # Run login loop
    login_win.mainloop()

open_login_window()
