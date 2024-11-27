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

# Create and place widgets
label = tk.Label(root, text="Enter User ID(s):")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

button = tk.Button(root, text="Grant Access", command=give_access)
button.pack(pady=10)

# Run the application
root.mainloop()
