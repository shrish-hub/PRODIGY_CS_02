from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to load an image
def load_image():
    global img, img_path
    img_path = filedialog.askopenfilename()
    if img_path:
        img = Image.open(img_path)
        
        # Check if the image is in 'P' mode and convert to 'RGB'
        if img.mode == 'P':
            img = img.convert('RGB')
            messagebox.showinfo("Info", "Image was in 'P' mode and has been converted to 'RGB'.")
        
        img.show()

# Function to save the image after encryption/decryption
def save_image(image):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        image.save(save_path)
        messagebox.showinfo("Success", "Image saved successfully!")

# Function to encrypt the image
def encrypt_image():
    if not img:
        messagebox.showerror("Error", "Please load an image first!")
        return
    key = int(entry_key.get()) % 256  # Limit key to 0-255
    encrypted_img = img.copy()  # Make a copy of the image
    pixels = encrypted_img.load()  # Access pixels

    # Check the image mode and process accordingly
    if img.mode == 'RGB':
        for i in range(encrypted_img.width):
            for j in range(encrypted_img.height):
                r, g, b = pixels[i, j]  # Get the RGB values
                pixels[i, j] = (r ^ key, g ^ key, b ^ key)  # XOR each color value with the key
    elif img.mode == 'RGBA':
        for i in range(encrypted_img.width):
            for j in range(encrypted_img.height):
                r, g, b, a = pixels[i, j]  # Get the RGBA values
                pixels[i, j] = (r ^ key, g ^ key, b ^ key, a)  # XOR RGB, keep alpha unchanged
    elif img.mode == 'L':  # Grayscale image (L mode)
        for i in range(encrypted_img.width):
            for j in range(encrypted_img.height):
                gray = pixels[i, j]  # Grayscale value
                pixels[i, j] = gray ^ key  # XOR the grayscale value with the key
    else:
        messagebox.showerror("Error", f"Unsupported image mode: {img.mode}")
        return

    encrypted_img.show()  # Show the encrypted image
    save_image(encrypted_img)  # Save the encrypted image

# Function to decrypt the image
def decrypt_image():
    if not img:
        messagebox.showerror("Error", "Please load an image first!")
        return
    key = int(entry_key.get()) % 256  # Same key must be used for decryption
    decrypted_img = img.copy()
    pixels = decrypted_img.load()

    # Check the image mode and process accordingly
    if img.mode == 'RGB':
        for i in range(decrypted_img.width):
            for j in range(decrypted_img.height):
                r, g, b = pixels[i, j]
                pixels[i, j] = (r ^ key, g ^ key, b ^ key)  # Reverse XOR for RGB values
    elif img.mode == 'RGBA':
        for i in range(decrypted_img.width):
            for j in range(decrypted_img.height):
                r, g, b, a = pixels[i, j]
                pixels[i, j] = (r ^ key, g ^ key, b ^ key, a)  # Reverse XOR RGB, keep alpha unchanged
    elif img.mode == 'L':  # Grayscale image (L mode)
        for i in range(decrypted_img.width):
            for j in range(decrypted_img.height):
                gray = pixels[i, j]  # Grayscale value
                pixels[i, j] = gray ^ key  # Reverse XOR for grayscale value
    else:
        messagebox.showerror("Error", f"Unsupported image mode: {img.mode}")
        return

    decrypted_img.show()  # Show the decrypted image
    save_image(decrypted_img)  # Save the decrypted image

# GUI setup using Tkinter
root = tk.Tk()
root.title("Image Encryption Tool")

# Load Image Button
btn_load = tk.Button(root, text="Load Image", command=load_image)
btn_load.pack(pady=10)

# Key Entry
label_key = tk.Label(root, text="Enter encryption/decryption key (0-255):")
label_key.pack(pady=5)

entry_key = tk.Entry(root, width=10)
entry_key.pack(pady=5)

# Encrypt Button
btn_encrypt = tk.Button(root, text="Encrypt Image", command=encrypt_image)
btn_encrypt.pack(pady=10)

# Decrypt Button
btn_decrypt = tk.Button(root, text="Decrypt Image", command=decrypt_image)
btn_decrypt.pack(pady=10)

# Start the GUI loop
root.mainloop()
