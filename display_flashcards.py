import tkinter as tk
from tkinter import ttk
import csv
import os
from PIL import Image, ImageTk

# Configure your paths and colors
csv_file_path = './output/translations.csv'
images_folder_path = './output'
nvidia_green = '#76b900'  # NVIDIA green color

# Load CSV data
flashcards = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        flashcards.append(row)

# Initialize tkinter
root = tk.Tk()
root.title("Flashcards")
root.configure(bg=nvidia_green)

# Global variable to keep track of the current flashcard index
current_index = 0

def load_image(image_file_name):
    """Load an image from the given path and return a PhotoImage object."""
    image_path = os.path.join(images_folder_path, image_file_name)
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 200))  # Resize to fit your layout
        return ImageTk.PhotoImage(image)
    return None

def update_flashcard():
    """Update the flashcard display with the current index."""
    global current_index
    if current_index < len(flashcards):
        flashcard = flashcards[current_index]
        word_label.config(text=flashcard['Primary Language Word'])
        translation_label.config(text=f"{flashcard['Learning Language']}: {flashcard['Translation']}")
        pronunciation_label.config(text=flashcard['Romanization'])
        
        image = load_image(flashcard['Image File Name'])
        image_label.config(image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection

def next_flashcard():
    """Move to the next flashcard."""
    global current_index
    current_index += 1
    if current_index >= len(flashcards):
        current_index = 0  # Loop back to the first flashcard
    update_flashcard()

# Labels for category, word, translation, and pronunciation
word_label = tk.Label(root, text='', fg='black', bg=nvidia_green, font=('Helvetica', 20))
word_label.pack(pady=10)

translation_label = tk.Label(root, text='', fg='black', bg=nvidia_green, font=('Helvetica', 16))
translation_label.pack(pady=5)

pronunciation_label = tk.Label(root, text='', fg='black', bg=nvidia_green, font=('Helvetica', 14))
pronunciation_label.pack(pady=5)

# Label for the image
image_label = tk.Label(root, bg=nvidia_green)
image_label.pack(pady=20)

# 'Next' button
next_button = ttk.Button(root, text='Next', command=next_flashcard)
next_button.pack(pady=20)
update_flashcard()  # Initialize the first flashcard

# Start the tkinter loop
root.mainloop()
