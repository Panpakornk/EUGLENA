import matplotlib
try:
    matplotlib.use('TkAgg') 
except:
    pass

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import os

def calculate_microns_per_pixel():
    print("--- Microscope Calibration Tool (Manual Input) ---")
    print("Due to window issues, please manually paste the file path.")
    print("1. Find your calibration image file.")
    print("2. Right-click the file and select 'Copy as path' (or simply drag and drop it here).")
    print("3. Paste it below and press Enter.")
    print("--------------------------------------------------")

    
    while True:
        file_path_input = input("Paste Image Path here: ").strip()
        
        file_path = file_path_input.strip('"').strip("'")
        
        if not file_path:
            continue
            
        if os.path.exists(file_path):
            break
        else:
            print(f"Error: File not found at: {file_path}")
            print("Please try again.")

    try:
        img = mpimg.imread(file_path)
    except Exception as e:
        print(f"Error reading image: {e}")
        return

    print("\nINSTRUCTIONS:")
    print("1. A window will open showing your image.")
    print("2. Click on the START point of the scale/grid.")
    print("3. Click on the END point.")
    print("   (Wait a moment after clicking for the red cross to appear)")
    print("------------------------------------------------")

    # Interactive plot
    try:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(img)
        ax.set_title("Click 2 points (Start & End) - Please wait for window")
        print("Waiting for user clicks...")
        
        # Use ginput to capture 2 clicks
        points = plt.ginput(n=2, timeout=-1, show_clicks=True)
        plt.close(fig)
    except Exception as e:
        print(f"Error launching plot window: {e}")
        return

    if not points or len(points) < 2:
        print("Error: You didn't click 2 points or closed the window too early.")
        return

    p1, p2 = points
    print(f"\nPoint 1: ({p1[0]:.2f}, {p1[1]:.2f})")
    print(f"Point 2: ({p2[0]:.2f}, {p2[1]:.2f})")

    # Calculate pixel distance
    pixel_dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    print(f"Pixel Distance: {pixel_dist:.2f} pixels")

    # Get real distance
    while True:
        try:
            print(f"\nMeasured pixel start: {p1}, end: {p2}")
            user_input = input(f"Enter the known distance for these {pixel_dist:.2f} pixels in MILLIMETERS (mm): ")
            real_dist_mm = float(user_input)
            if real_dist_mm <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Calculate ratio
    mm_per_pixel = real_dist_mm / pixel_dist

    print("\n" + "="*50)
    print(f"CALIBRATION RESULT")
    print("-" * 50)
    print(f"Known Distance: {real_dist_mm} mm")
    print(f"Measured Pixels: {pixel_dist:.2f} px")
    print(f"Scale Factor:    {mm_per_pixel:.9f} mm/px")
    print("="*50)
    print("\n>>> Copy this line to update your Notebook: <<<")
    print(f"MILLIMETERS_PER_PIXEL = {mm_per_pixel:.9f}")
    print("\n" + "="*50)

if __name__ == "__main__":
    calculate_microns_per_pixel()
