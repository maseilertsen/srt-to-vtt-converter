# Filename:         srt-to-vtt-converter_v01
# Author:           Marius Eilertsen
# Conversion code:  Anders Martin Helle
#
# Last modified: 15.10.2024
#
# This program converts .srt-format files to .vtt-format
# via a drag and drop window.

import os
import tkinter as tk
from tkinter import Button                     
from pathlib import Path                       # Construct path from string.
from tkinter import filedialog                 # File browser function.
from tkinterdnd2 import TkinterDnD, DND_FILES  # Drag and drop functionality.

vttFilePath = ''  # initiate empty path

# Converting .srt to .vtt
def process_file(filePath):
    global vttFilePath
    try:
        with open(filePath, 'r') as file: 
            srt = file.read()               # Original onversion code by
            vtt = "WEBVTT \n\n"             # Anders Martin Helle (line 25-35). 
                                            
            for line in srt.splitlines():
                if line.isnumeric() :
                    continue
                if "-->" in line:
                    line = line.replace(',', '.')
                    vtt += line + '\n'
                else:
                    vtt += line + '\n'

            baseName = os.path.basename(filePath)            # Getting name from file.
            full_path = os.path.join(vttFilePath, baseName) # Joining path and filename.
            vtt_path = full_path.replace(".srt", ".vtt")

            with open(vtt_path, 'w') as file:
                file.write(vtt)

    except Exception as e:
        outputText.insert(tk.END, "Error reading\n")

# Set output directory
def browse_button():
    global outputDirectory, vttFilePath
    outputDirectory = filedialog.askdirectory()
    vttFilePath = outputDirectory                     # When output is set from button before drop.
    outputText.insert(tk.END, "Destination folder: " +
                       str(vttFilePath) + '\n')       # Display output folder in window.
    return outputDirectory
    
# Collect paths to files and send tem to processing
def on_drop(event):
    global droppedFilePath, vttFilePath
    
    filePaths = event.data.split()    # collects all files paths in array
    droppedFilePath = event.data    # used in functions

    if not vttFilePath:
        vttFilePath = browse_button() # Output directory

    for filePath in filePaths:
        if os.path.isdir(filePath):   # Checks if file is a folder.
            for root, dirs, files in os.walk(filePath):
                for fileName in files:
                    fileFullPath = os.path.join(root, fileName)
                    if fileFullPath.endswith(".srt"):
                        process_file(fileFullPath)
                for dirName in dirs:
                    sub_dir_path = Path(os.path.join(root, dirName))
                    on_drop_simple([sub_dir_path])  # Recursively process subdirectories
        elif filePath.endswith(".srt"):
            process_file(filePath)
        else:
            print("") # Left in for debugging purposes.


# Helper to recursively process subdirectories
# (The main 'on_drop' function takes more avanced parameters.)
def on_drop_simple(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for fileName in files:
                    fileFullPath = os.path.join(root, fileName)
                    if fileFullPath.endswith(".srt"):
                        process_file(fileFullPath)
                for dir_name in dirs:
                    subDirPath = os.path.join(root, dir_name)
                    on_drop_simple([subDirPath])
        elif path.endswith(".srt"):
            process_file(path)
# Resets export path and clears window of text.
def reset():
    global vttFilePath
    vttFilePath = ''
    outputText.delete("1.0","end") # removes all text in window. 
    outputText.pack()


# Setting up the main window
window = TkinterDnD.Tk() # Create a TkinterDnD window
window.title(".srt->.vtt File Processor")

# Label above drop area
label = tk.Label(window, text="Drag and drop .srt files here")
label.pack(pady=10) # padding in y-direction. 

# Output text properties (text inside drop window).
outputText = tk.Text(window, wrap="word", height=15, width=60)
outputText.pack(padx=10, pady=10)


# Bind the drag-and-drop event
window.drop_target_register(DND_FILES)
window.dnd_bind("<<Drop>>", on_drop)

# Button for output path
browseButton = Button(text="Output directory", command=browse_button)
browseButton.pack(pady=5)

# Button to reset folder path
resetButton = Button(text="Reset", command=reset)
resetButton.pack(pady=5)

# Start the application
window.mainloop()