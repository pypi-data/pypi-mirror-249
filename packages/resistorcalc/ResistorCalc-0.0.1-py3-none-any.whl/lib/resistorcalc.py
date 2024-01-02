#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import os

def show_about():
    os_info = os.uname()

    # Format the OS information
    os_details = f"OS: {os_info.sysname} {os_info.machine} {os_info.release}"

    messagebox.showinfo("About", f"ResistorCalc\nVersion 0.0.1\nAuthor: Hariharan C\n\n{os_details}")

def about_resistor():
    print("All about resistor")

# Resistor calculation functions
def calculate_resistor_value(colors, num_bands):
    # Mapping of color names to numeric values
    color_mapping = {
        'black': 0, 'brown': 1, 'red': 2, 'orange': 3,
        'yellow': 4, 'green': 5, 'blue': 6, 'violet': 7,
        'gray': 8, 'white': 9
    }

    # Validate the number of colors provided matches the selected number of bands
    if len(colors) != num_bands:
        raise ValueError(f"Expected {num_bands} colors, but got {len(colors)} colors.")

    # Resistor calculation logic based on the number of bands
    if num_bands == 4:
        significant_digits = color_mapping[colors[0]] * 10 + color_mapping[colors[1]]
        multiplier = 10 ** color_mapping[colors[2]]
        tolerance = None

        if len(colors) == 4:
            tolerance_mapping = {'gold': 5, 'silver': 10}
            tolerance = tolerance_mapping.get(colors[3])

        resistance_value = significant_digits * multiplier

    elif num_bands == 5:
        significant_digits = color_mapping[colors[0]] * 100 + color_mapping[colors[1]] * 10 + color_mapping[colors[2]]
        multiplier = 10 ** color_mapping[colors[3]]
        tolerance = None

        if len(colors) == 5:
            tolerance_mapping = {'gold': 5, 'silver': 10}
            tolerance = tolerance_mapping.get(colors[4])

        resistance_value = significant_digits * multiplier

    elif num_bands == 6:
        significant_digits = color_mapping[colors[0]] * 100 + color_mapping[colors[1]] * 10 + color_mapping[colors[2]]
        multiplier = 10 ** color_mapping[colors[3]]
        tolerance = None

        if len(colors) == 6:
            temperature_coefficient_mapping = {'brown': 100, 'red': 50, 'orange': 15, 'yellow': 25}
            temperature_coefficient = temperature_coefficient_mapping.get(colors[4])
            tolerance_mapping = {'gold': 5, 'silver': 10}
            tolerance = tolerance_mapping.get(colors[5])

        resistance_value = significant_digits * multiplier

    return resistance_value, tolerance

# GUI setup functions

def visualize_color_code(colors):
    canvas.configure(bg='#1a1a1a')
    # Define color codes and positions for visualization
    color_codes = colors[:3]
    color_positions = [(100, 52), (150, 52), (200, 52)]

    # Clear the previous content of the canvas
    canvas.delete("all")

    # Draw rectangles with corresponding colors
    for code, position in zip(color_codes, color_positions):
        canvas.create_rectangle(position[0], position[1], position[0] + 50, position[1] + 50, fill=code, outline='black')

    # Draw horizontal terminals and rounded rectangle
    canvas.create_rectangle(44, 80, 99, 75, fill='#d0d5db', outline='#d0d5db')  # Left terminal
    canvas.create_rectangle(295, 75, 350, 80, fill='#d0d5db', outline='#d0d5db')  # Right terminal
    canvas.create_rectangle(100, 52, 300, 100, fill='', outline='silver', width=1)  # Rounded rectangle

    # Check if the last color is gold or silver and draw the tolerance band
    last_color = colors[-1]
    if last_color == 'gold' or last_color == 'silver':
        tolerance_width = 50
        tolerance_height = 50
        tolerance_position = (250, 52)
        canvas.create_rectangle(tolerance_position[0], tolerance_position[1],
                                tolerance_position[0] + tolerance_width, tolerance_position[1] + tolerance_height,
                                fill=last_color, outline='black')

def clear_fields():
    entry.delete(0, tk.END)
    result_label.config(text="")
    canvas.delete("all")

def on_calculate():
    # Get user input from the entry field
    color_input = entry.get().lower().split()
    # Get the number of bands selected by the user
    num_bands = bands_var.get()

    # Check if the user provided valid input and selected the number of bands
    if not color_input or num_bands not in (4, 5, 6):
        result_label.config(text="Error: Enter valid color bands and select the number of bands.")
        return

    try:
        # Calculate resistor value and tolerance based on user input
        resistance, tolerance = calculate_resistor_value(color_input, num_bands)

        # Convert to kiloohms if resistance is in the kiloohm range
        if resistance >= 1000:
            resistance /= 1000
            unit = 'kilo ohms'
        else:
            unit = 'ohms'

        # Display the calculated values in the result_label
        result_label.config(
            text=f"Resistor Value: {resistance} {unit}\n\nTolerance: +/- {tolerance}%" if tolerance is not None
            else f"Resistor Value: {resistance} {unit}")

        # Set focus to the root window to enable Enter key globally
        root.focus_set()

        # Visualize the color code
        visualize_color_code(color_input)

    except (KeyError, ValueError) as e:
        # Handle invalid color input or calculation errors
        result_label.config(text=str(e))

# GUI setup

root = tk.Tk()
root.title("Resistor Calculator")

# Get screen resolution for window size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# Set background color and load app icon
root.configure(bg='black')
icon_path = "../banner/app_icon.png"
icon_image = tk.PhotoImage(file=icon_path)
root.tk.call('wm', 'iconphoto', root._w, icon_image)

# Label for resistor code visualizer
label_vizualizer = tk.Label(root, text="Resistor Code Visualizer", bg='black', fg='gold', font=('Helvetica', 18))
label_vizualizer.pack(padx=30, pady=30)

# Create a canvas to visualize the color code
canvas_width = 400
canvas_height = 150
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black')
canvas.pack(padx=30, pady=20)

# Label for band selection instruction
label_band_select = tk.Label(root, text='Select the resistor color band before entering the color\n', bg='black', fg='gold', font=('Helvetica', 14))
label_band_select.pack(padx=0, pady=0)

# Variable to store the number of bands selected by the user
bands_var = tk.IntVar()

# Checkboxes for selecting the number of bands
four_band_checkbox = tk.Checkbutton(root, text="4 Bands", variable=bands_var, onvalue=4, offvalue=0, font=('Arial', 14))
four_band_checkbox.configure(bg='#333333')
four_band_checkbox.pack(side=tk.TOP, padx=(0, 20), pady=(10, 0), anchor=tk.CENTER)

five_band_checkbox = tk.Checkbutton(root, text="5 Bands", variable=bands_var, onvalue=5, offvalue=0, font=('Arial', 14))
five_band_checkbox.configure(bg='#333333')
five_band_checkbox.pack(side=tk.TOP, padx=(0, 20), pady=(10, 0), anchor=tk.CENTER)

six_band_checkbox = tk.Checkbutton(root, text="6 Bands", variable=bands_var, onvalue=6, offvalue=0, font=('Arial', 14))
six_band_checkbox.configure(bg='#333333')
six_band_checkbox.pack(side=tk.TOP, padx=(0, 20), pady=(10, 0), anchor=tk.CENTER)

# Label for entering color bands
label = tk.Label(root, text="\nEnter the color bands of the resistor, separated by spaces:", bg='black', fg='gold', font=('Helvetica', 18))
label.pack(padx=0, pady=0)

# Entry field for user input
entry = tk.Entry(root, width=30, font=('Helvetica', 18), bg='white')
entry.configure(bg='white')
entry.pack(padx=0, pady=20)

# Bind events to entry field for text selection color change
entry.bind('<FocusIn>', lambda event: entry.config(fg='black', selectbackground='yellow'))
entry.bind('<FocusOut>', lambda event: entry.config(fg='black', selectbackground='white'))

# Label to display the result
result_label = tk.Label(root, text="", bg='black', fg='white', font=('Helvetica', 18))
result_label.pack(side=tk.TOP, padx=(100, 100), pady=(10, 0), anchor=tk.CENTER)

# Button to trigger the calculation and visualization
calculate_button = tk.Button(root, text="Calculate", command=on_calculate, bg='white', fg='black', font=('Arial', 18))
calculate_button.configure(bg='#ffcc00')
calculate_button.pack(side=tk.LEFT, padx=(800, 0), pady=(10, 0), anchor=tk.CENTER)

# Button to clear all fields
clear_button = tk.Button(root, text="Clear", command=clear_fields, bg='white', fg='black', font=('Arial', 18))
clear_button.configure(bg='#ffcc00')
clear_button.pack(side=tk.LEFT, padx=(100, 0), pady=(10, 0), anchor=tk.CENTER)

# Bind the <Return> key to the on_calculate function
root.bind('<Return>', lambda event: on_calculate())


# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create an About menu
about_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=about_menu, command=show_about)

# Create an All about resistor menu

know_res = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label='Resistor', menu=know_res, command=about_resistor)

# Add menu item to the About menu
about_menu.add_command(label="About", command=show_about)

# Add menu item to the Resistor
about_menu.add_command(label='Know Resistor', command=about_resistor)


# Start the Tkinter event loop
root.mainloop()
