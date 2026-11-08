# File Organizer & Cleanup Utility
#Sorts the files in a folder into a category subfoders based on their extension 
import os
import shutil
import logging

# Settings
# Use a folder next to this script, so it works from any terminal location
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
folder= os.path.join(BASE_DIR,"test_folder")

# Write every action to a log file with date and time
logging.basicConfig(
    filename=os.path.join(BASE_DIR,"organizer.log"), 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)

# Extenion to category folder 
categories={".pdf":"Documents",
            ".txt":"Documents",
            ".docx":"Documents",
            ".jpg":"Images",
            ".jpeg":"Images",
            ".png":"Images", 
            ".mp4":"Videos",
            ".mkv":"Videos",
            ".zip":"Archives",
            ".rar":"Archives",
            ".py":"Code",
            ".html":"Code"}

# Stop early if the folder does not exist
if not os.path.isdir(folder):
    print("Folder not found. Create a folder named 'test_folder' next to organizer.py.")
    exit()
# Counter for final suummary
moved=0
failed=0

# main loop
for name in os.listdir(folder):
    full_path= os.path.join(folder,name)

    # Skip folders, only moves files
    if not os.path.isfile(full_path):
         continue

# Find the category from the extension
    base, ext=os.path.splitext(name)
    category=categories.get(ext,"others")

# Create the category folder if it doesnot exist
    target= os.path.join(folder,category)
    os.makedirs(target, exist_ok=True)

    # Handing name collisions: photo.jpg -> photo_1.jpg
    destination=os.path.join(target, name)
    counter=1
    while os.path.exists(destination):
         new_name=f"{base}_{counter}{ext}"
         destination=os.path.join(target,new_name)
         counter +=1 

    # Move the file and record the result
    try:
     shutil.move(full_path, destination)
     print("Moved:",name, "->",category)
     moved += 1
    except PermissionError:
        print("permission denied:", name)
        logging.error(f"permission denied:, {name}")
        failed += 1
    except Exception as e:
        print("Error with", name,":",e)
        logging.error(f"Error with {name}:{e}")
        failed += 1
#   Summary
print("\n===== Summary ======")  
print(f"files moved: {moved}")
print(f"files failed: {failed}") 
logging.info(f" Summary: {moved} moved , {failed} failed")
