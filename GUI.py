import tkinter as tk
from tkinter import messagebox

def give_access():
    user_ids = entry.get()
    if not user_ids.strip():
        messagebox.showerror("Error", "Please enter at least one User ID.")
        return
    
    # Split the input into a list of user IDs
    user_id_list = [user_id.strip() for user_id in user_ids.split(",")]
    
    # Simulate granting access (replace this with actual logic)
    for user_id in user_id_list:
        print(f"Access granted to User ID: {user_id}")
    
    # Display success message
    messagebox.showinfo("Success", f"Access granted to: {', '.join(user_id_list)}")

# Create the main window
root = tk.Tk()
root.title("User Access Management")

# Set the size of the window (covers more screen space)
root.geometry("800x400")  # Width x Height

# Create and place widgets with larger input field
label = tk.Label(root, text="Enter User ID(s):", font=("Arial", 18))
label.pack(pady=(20, 10))  # Top and bottom padding

entry = tk.Entry(root, font=("Arial", 16), width=80)  # Larger input field
entry.pack(pady=(10, 20))  # Top and bottom padding

button = tk.Button(root, text="Grant Access", font=("Arial", 16), command=give_access)
button.pack(pady=20)

# Add some extra padding to the entire window
for widget in [label, entry, button]:
    widget.pack_configure(padx=40)

# Run the application
root.mainloop()
