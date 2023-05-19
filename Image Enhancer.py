import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image
import numpy as np
import os
from tqdm import tqdm


def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(tk.END, folder_path)


def enhance_image_quality(image_path):
    try:
        # Load the image using PIL
        image = Image.open(image_path)

        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform image enhancement operations using OpenCV
        enhanced_image = cv2.resize(image_cv, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        enhanced_image = cv2.GaussianBlur(enhanced_image, (0, 0), sigmaX=1, sigmaY=1)

        # Convert the enhanced image back to PIL format
        enhanced_image_pil = Image.fromarray(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))

        # Save the enhanced image
        output_path = os.path.splitext(image_path)[0] + "_enhanced.jpg"
        enhanced_image_pil.save(output_path)

        # Delete the original image
        os.remove(image_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def enhance_images_in_folder():
    folder_path = folder_path_entry.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder.")
        return

    try:
        # Get a list of all image files in the folder
        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Initialize the progress bar
        progress_bar["maximum"] = len(image_files)
        progress_bar["value"] = 0

        # Process each image in the folder
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            enhance_image_quality(image_path)
            progress_bar["value"] += 1
            window.update()

        messagebox.showinfo("Enhancement Complete", "Image enhancement completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
window = tk.Tk()
window.title("Image Enhancement")
window.geometry("600x320")
window.configure(bg="#2b2b2b")  # Set background color

# Set a custom style for the window
style = ttk.Style(window)
style.theme_use('clam')  # Use the 'clam' theme
style.configure("TFrame", background="#2b2b2b")  # Set frame background color
style.configure("TButton", background="#51a1cc", foreground="#ffffff", font=("Arial", 12, "bold"))
style.map("TButton",
          background=[("active", "#51a1cc"), ("pressed", "#3986a3")],  # Set button colors for different states
          foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])
style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Arial", 12))
style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

# Create a frame to hold the content
content_frame = ttk.Frame(window)
content_frame.pack(pady=20)

# Create and pack the title label
title_label = ttk.Label(content_frame, text="Image Enhancement", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the folder selection button
folder_button = ttk.Button(content_frame, text="Select Folder", command=select_folder)
folder_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the folder path entry field
folder_path_entry = ttk.Entry(content_frame)
folder_path_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Create and pack the enhance button
enhance_button = ttk.Button(content_frame, text="Enhance Images", command=enhance_images_in_folder)
enhance_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", style="green.Horizontal.TProgressbar")
progress_bar.pack(pady=20)

# Center the window on the screen
window.eval('tk::PlaceWindow . center')

# Set the style for the progress bar when it is increasing
style.configure("green.Horizontal.TProgressbar",
                troughcolor="#2b2b2b",  # Set the color of the progress bar trough
                background="#4caf50",  # Set the color of the progress bar
                bordercolor="#4caf50"  # Set the color of the progress bar border
                )

# Run the main window event loop
window.mainloop()