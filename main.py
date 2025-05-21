import os
from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Generate encryption key if not exists
def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

# Encrypt file
def encrypt_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)

    os.makedirs("encrypted_files", exist_ok=True)
    filename = os.path.basename(filepath)
    with open(f'encrypted_files/{filename}.enc', 'wb') as enc_file:
        enc_file.write(encrypted)
    messagebox.showinfo("Success", f"Encrypted: {filename}")

# Decrypt file
def decrypt_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, 'rb') as enc_file:
        encrypted = enc_file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception as e:
        messagebox.showerror("Error", "Invalid file or key!")
        return

    os.makedirs("decrypted_files", exist_ok=True)
    filename = os.path.basename(filepath).replace('.enc', '')
    with open(f'decrypted_files/{filename}', 'wb') as dec_file:
        dec_file.write(decrypted)
    messagebox.showinfo("Success", f"Decrypted: {filename}")

# GUI Setup
generate_key()
root = Tk()
root.title("File Encryption & Decryption System")
root.geometry("400x250")
Label(root, text="Secure File Encryption Tool", font=("Arial", 14)).pack(pady=20)
Button(root, text="🔒 Encrypt File", command=encrypt_file, width=30, bg="green", fg="white").pack(pady=10)
Button(root, text="🔓 Decrypt File", command=decrypt_file, width=30, bg="blue", fg="white").pack(pady=10)
Button(root, text="❌ Exit", command=root.destroy, width=30, bg="red", fg="white").pack(pady=10)
root.mainloop()
