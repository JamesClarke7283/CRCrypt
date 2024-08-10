import tkinter as tk
import customtkinter as ctk
import pygame
from pygame import Color
from src.core import CRCrypt, RubikCube, Step
from src.logging import get_logger

logger = get_logger()

class CRCryptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CRCrypt - Rubik's Cube Cryptography")

        # Initialize Pygame for drawing
        pygame.init()
        self.colors = [Color("red"), Color("green"), Color("blue"), Color("orange"), Color("white"), Color("yellow")]

        # Set up the cube dimension variable
        self.cube_dim_var = tk.IntVar(value=4)

        # Set up the delay variable for animations
        self.delay_var = tk.IntVar(value=500)

        # Set up the key and message variables
        self.key_var = tk.StringVar()
        self.message_var = tk.StringVar()

        # Create GUI layout
        self.setup_gui()

        # Initialize the Rubik's cube
        self.cube = RubikCube(dimension=self.cube_dim_var.get())

        # Display the initial solved state of the cube
        self.draw_cube()

    def setup_gui(self):
        # Canvas for cube visualization
        self.canvas = ctk.CTkCanvas(self.root, width=720, height=720)  # Adjusted to fit full cube
        self.canvas.grid(row=0, column=0, rowspan=6, padx=20, pady=20)

        # Key entry (scrollable text box)
        key_label = ctk.CTkLabel(self.root, text="Key:")
        key_label.grid(row=0, column=1, sticky="e")
        self.key_entry = ctk.CTkTextbox(self.root, width=400, height=50)  # Scrollable text box
        self.key_entry.grid(row=0, column=2, padx=20, pady=5)
        
        # Message/Ciphertext entry (scrollable text box)
        message_label = ctk.CTkLabel(self.root, text="Message/Ciphertext:")
        message_label.grid(row=1, column=1, sticky="e")
        self.message_entry = ctk.CTkTextbox(self.root, width=400, height=100)  # Scrollable text box
        self.message_entry.grid(row=1, column=2, padx=20, pady=5)

        # Encrypt button
        encrypt_button = ctk.CTkButton(self.root, text="Encrypt", command=self.encrypt)
        encrypt_button.grid(row=2, column=2, padx=20, pady=10, sticky="w")

        # Decrypt button
        decrypt_button = ctk.CTkButton(self.root, text="Decrypt", command=self.decrypt)
        decrypt_button.grid(row=2, column=2, padx=20, pady=10, sticky="e")

        # Cube dimension setting
        cube_dim_label = ctk.CTkLabel(self.root, text="Cube Dimension:")
        cube_dim_label.grid(row=3, column=1, sticky="e")
        cube_dim_entry = ctk.CTkEntry(self.root, textvariable=self.cube_dim_var, width=400)
        cube_dim_entry.grid(row=3, column=2, padx=20, pady=5)

        # Delay setting for animation
        delay_label = ctk.CTkLabel(self.root, text="Animation Delay (ms):")
        delay_label.grid(row=4, column=1, sticky="e")
        delay_entry = ctk.CTkEntry(self.root, textvariable=self.delay_var, width=400)
        delay_entry.grid(row=4, column=2, padx=20, pady=5)

        # Update button to redraw the cube
        update_button = ctk.CTkButton(self.root, text="Update Cube", command=self.update_cube)
        update_button.grid(row=5, column=2, padx=20, pady=10)

    def update_cube(self):
        self.cube = RubikCube(dimension=self.cube_dim_var.get())
        self.draw_cube()

    def encrypt(self):
        key = self.key_entry.get("1.0", tk.END).strip()
        message = self.message_entry.get("1.0", tk.END).strip()

        if not key or not message:
            logger.error("Key and message cannot be empty.")
            return

        crcrypt = CRCrypt(key=key, cube_dim=self.cube_dim_var.get())
        encrypted_message = crcrypt.encrypt(message)

        # Get the steps to animate
        steps = crcrypt.code_generator.key_encode()
        self.animate_steps(steps)

        # Update the message field with the ciphertext
        self.message_entry.delete("1.0", tk.END)
        self.message_entry.insert(tk.END, encrypted_message)

    def decrypt(self):
        key = self.key_entry.get("1.0", tk.END).strip()
        ciphertext = self.message_entry.get("1.0", tk.END).strip()

        if not key or not ciphertext:
            logger.error("Key and ciphertext cannot be empty.")
            return

        crcrypt = CRCrypt(key=key, cube_dim=self.cube_dim_var.get())

        # Get the steps to animate for decryption (reverse the encoding steps)
        steps = crcrypt.code_generator.key_decode()
        
        # Reset the cube to the initial solved state before applying reverse steps
        self.cube = RubikCube(dimension=self.cube_dim_var.get())

        # Animate the decryption process
        self.animate_steps(steps, reverse=True)

        # Perform the decryption
        decrypted_message = crcrypt.decrypt(ciphertext)

        # Update the message field with the plaintext
        self.message_entry.delete("1.0", tk.END)
        self.message_entry.insert(tk.END, decrypted_message)


    def apply_step(self, cube, step):
        # Perform the move on the cube
        cube.move(step)
        return cube

    def animate_steps(self, steps, reverse=False):
        if reverse:
            steps = reversed(steps)

        try:
            # Attempt to get the delay value and convert it to an integer
            delay = int(self.delay_var.get())
        except (ValueError, TclError):
            # If there is an issue, default to a reasonable delay value, e.g., 500 ms
            delay = 500

        for step in steps:
            self.cube = self.apply_step(self.cube, step)
            self.draw_cube()
            self.root.update()
            self.root.after(delay)



    def draw_cube(self):
        self.canvas.delete("all")
        square_size = 40

        # Convert Pygame colors to hex strings for Tkinter
        def color_to_hex(color):
            return '#{:02x}{:02x}{:02x}'.format(color.r, color.g, color.b)

        # Define the positions of the faces on a 2D plane
        face_positions = [
            (1, 1),  # Face 0 (Top)
            (0, 1),  # Face 1 (Left)
            (1, 2),  # Face 2 (Front)
            (1, 0),  # Face 3 (Back)
            (2, 1),  # Face 4 (Bottom)
            (1, 3)   # Face 5 (Right)
        ]

        for face in range(6):
            start_x, start_y = face_positions[face]
            for i in range(self.cube_dim_var.get()):
                for j in range(self.cube_dim_var.get()):
                    x1 = (start_x * self.cube_dim_var.get() + j) * square_size
                    y1 = (start_y * self.cube_dim_var.get() + i) * square_size
                    x2 = x1 + square_size
                    y2 = y1 + square_size
                    color = color_to_hex(self.colors[self.cube.cube[face][i, j]])
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def main():
    root = ctk.CTk()
    app = CRCryptGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
