import tkinter as tk
from tkinter import ttk
import subprocess

# Initialize global variables
user_data = {}
categories = ['Fruit']
languages = sorted(['English', 'Deutsch (German)', '日本語 (Japanese)', '한국어 (Korean)', 'नेपाली (Nepali)', 'हिन्दी (Hindi)'])
nvidia_green = '#76b900'  # NVIDIA green color

def generate_flashcards():
    # Placeholder for the function to call a separate Python program
    print("Generating flashcards...", user_data)
    # Convert list to a string format that can be parsed by the receiving script
    categories_str = ','.join(categories)  # Join list items into a single string separated by commas
    learning_str = ','.join(user_data['Learning Languages'])
    # Prepare the command to run the script with parameters
    command = [
        'python',
        '.\generate_flashcard_content.py',
        user_data['Name'],
        user_data['Primary Language'],
        learning_str,
        categories_str
    ]
    # Run the command
    subprocess.run(command)

def close_application():
    global root
    root.destroy()

# Clear the current content of the root window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Function to open the Generate Flashcards screen
def open_generate_flashcards_screen():
    global root, user_data, categories
    root.destroy()

    root = tk.Tk()
    root.title("Generate Flashcards Screen")
    root.configure(bg='black')

    # Adjusted labels with anchor='w' for left alignment and fill='x' to fill the horizontal space
    tk.Label(root, text=f"Name: {user_data.get('Name', 'Unknown')}", fg=nvidia_green, bg='black', anchor='w').pack(fill='x', pady=5)
    tk.Label(root, text=f"Primary Language: {user_data.get('Primary Language', 'Unknown')}", fg=nvidia_green, bg='black', anchor='w').pack(fill='x', pady=5)
    tk.Label(root, text="Learning Languages:", fg=nvidia_green, bg='black', anchor='w').pack(fill='x', pady=5)
    for language in user_data.get('Learning Languages', []):
        tk.Label(root, text=f"- {language}", fg=nvidia_green, bg='black', anchor='w').pack(fill='x')
    tk.Label(root, text="Selected Categories:", fg=nvidia_green, bg='black', anchor='w').pack(fill='x', pady=5)
    for category in categories:
        tk.Label(root, text=f"- {category}", fg=nvidia_green, bg='black', anchor='w').pack(fill='x')

    # 'Generate Flashcards' button
    tk.Button(root, text='Generate Flashcards', command=generate_flashcards, fg='white', bg=nvidia_green, font=('Helvetica', '10', 'bold')).pack(pady=10)

    # 'Close' button
    tk.Button(root, text='Close', command=close_application, fg='white', bg=nvidia_green, font=('Helvetica', '10', 'bold')).pack(pady=10)


def prepare_for_categories_screen():
    global user_data
    # Ensure user_data is populated with the 'Name' and other details here
    user_data = {
        'Name': name_var.get(),
        'Primary Language': primary_lang_var.get(),
        'Learning Languages': [lang for lang in languages if learning_langs_var[lang].get()]
    }
    open_category_selection_screen()

# Function to open the Category Selection screen
def open_category_selection_screen():
    clear_window()  # Clear the current window content
    root.title("Category Selection")

    # Variable declarations for this screen
    new_category_var = tk.StringVar()
    remove_category_var = tk.StringVar()

    # Frame for adding a new category
    add_category_frame = tk.Frame(root, bg='black')
    add_category_frame.pack(pady=10)
    tk.Entry(add_category_frame, textvariable=new_category_var).pack(side='left', padx=5)
    tk.Button(add_category_frame, text='Add Category', command=lambda: add_category(new_category_var), fg='black', bg=nvidia_green).pack(side='left', padx=5)

    # Frame for removing a category
    remove_category_frame = tk.Frame(root, bg='black')
    remove_category_frame.pack(pady=10)
    remove_category_combobox = ttk.Combobox(remove_category_frame, textvariable=remove_category_var, values=categories)
    remove_category_combobox.pack(side='left', padx=5)
    tk.Button(remove_category_frame, text='Remove Category', command=lambda: remove_category(remove_category_var, remove_category_combobox), fg='black', bg=nvidia_green).pack(side='left', padx=5)

    # Frame for displaying categories
    categories_frame = tk.Frame(root, bg='black')
    categories_frame.pack(pady=10)
    update_categories_display(categories_frame)

    # 'Next' button to proceed to the final screen
    tk.Button(root, text='Next', command=open_generate_flashcards_screen, fg='white', bg=nvidia_green, font=('Helvetica', '10', 'bold')).pack(pady=10)

# Function to add a category
def add_category(new_category_var):
    new_category = new_category_var.get().strip()
    if new_category and new_category not in categories:
        categories.append(new_category)
        new_category_var.set('')  # Clear the input field
        open_category_selection_screen()  # Refresh the category selection screen

# Function to remove a category
def remove_category(remove_category_var, remove_category_combobox):
    category_to_remove = remove_category_var.get()
    if category_to_remove in categories:
        categories.remove(category_to_remove)
        remove_category_var.set('')  # Clear the combobox selection
        open_category_selection_screen()  # Refresh the category selection screen

# Function to update the categories display
def update_categories_display(categories_frame):
    for widget in categories_frame.winfo_children():
        widget.destroy()
    for category in categories:
        tk.Label(categories_frame, text=category, fg=nvidia_green, bg='black').pack()

# Function to open the initial screen
def open_initial_screen():
    clear_window()  # Clear the current window content
    root.title("Language Learning Helper")

    # Widgets for collecting user data
    tk.Label(root, text='Name', fg=nvidia_green, bg='black').grid(row=0, column=0, sticky='w', columnspan=2)
    tk.Entry(root, textvariable=name_var).grid(row=0, column=1, sticky='w', padx=(5, 0))

    tk.Label(root, text='Primary Language', fg=nvidia_green, bg='black').grid(row=1, column=0, sticky='w', columnspan=2)
    primary_lang_menu = ttk.Combobox(root, textvariable=primary_lang_var, values=languages, state="readonly")
    primary_lang_menu.grid(row=1, column=1, sticky='w', columnspan=4)
    primary_lang_menu.current(0)

    tk.Label(root, text='Learning Languages', fg=nvidia_green, bg='black').grid(row=2, column=0, sticky='w', columnspan=6)
    for i, lang in enumerate(languages):
        tk.Checkbutton(root, text=lang, variable=learning_langs_var[lang], bg='black', fg=nvidia_green, selectcolor='black').grid(row=3+i//3, column=i%3, sticky='w')

    # 'Next' button to proceed
    tk.Button(root, text='Next', command=prepare_for_categories_screen, fg='white', bg=nvidia_green, font=('Helvetica', '10', 'bold')).grid(row=10, column=2, sticky='e', padx=10)

# Main application setup
root = tk.Tk()
root.configure(bg='black')

# Variable declarations
name_var = tk.StringVar()
primary_lang_var = tk.StringVar()
learning_langs_var = {lang: tk.BooleanVar() for lang in languages}

open_initial_screen()  # Open the initial screen

root.mainloop()
