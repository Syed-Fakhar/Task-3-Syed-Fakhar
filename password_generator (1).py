import random
import string
import math
import customtkinter as ctk
import tkinter.messagebox as messagebox

# Set up appearance mode and default color theme
ctk.set_appearance_mode("System")  # Matches user's system theme (Light or Dark)
ctk.set_default_color_theme("blue")  # Modern blue theme

class PasswordGeneratorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("FAKHAR SECURITY CORE - Password Generator")
        self.geometry("480x640")
        self.resizable(False, False)
        
        # App Title Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(padx=20, pady=(25, 10), fill="x")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🔑 FAKHAR SECURITY CORE", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        )
        self.title_label.pack(anchor="center")
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, 
            text="Advanced Password Generation Utility", 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#6B7280", "#9CA3AF")
        )
        self.subtitle_label.pack(anchor="center", pady=(2, 0))
        
        # Frame for password options (Interior Improvements)
        # Added a clean border and corner radius to behave like a card container
        self.options_frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            border_width=1,
            border_color=("#E5E7EB", "#374151")
        )
        self.options_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Slider section for password length
        self.length_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.length_frame.pack(padx=20, pady=(15, 5), fill="x")
        
        self.length_label = ctk.CTkLabel(
            self.length_frame, 
            text="Password Length: 12", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        self.length_label.pack(side="left")
        
        self.length_slider = ctk.CTkSlider(
            self.options_frame, 
            from_=6, 
            to=32, 
            number_of_steps=26,  # 32 - 6 = 26 steps
            command=self.update_length_label,
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            progress_color="#3B82F6"
        )
        self.length_slider.set(12)  # Default length
        self.length_slider.pack(padx=20, pady=5, fill="x")
        
        # Checkboxes for custom character sets (Styled neatly)
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.uppercase_cb = ctk.CTkCheckBox(
            self.options_frame, 
            text="Include Uppercase Letters (A-Z)", 
            variable=self.uppercase_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            command=self.generate_password,
            checkmark_color="#FFFFFF",
            fg_color="#3B82F6",
            hover_color="#2563EB"
        )
        self.uppercase_cb.pack(padx=25, pady=8, anchor="w")
        
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.lowercase_cb = ctk.CTkCheckBox(
            self.options_frame, 
            text="Include Lowercase Letters (a-z)", 
            variable=self.lowercase_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            command=self.generate_password,
            checkmark_color="#FFFFFF",
            fg_color="#3B82F6",
            hover_color="#2563EB"
        )
        self.lowercase_cb.pack(padx=25, pady=8, anchor="w")
        
        self.numbers_var = ctk.BooleanVar(value=True)
        self.numbers_cb = ctk.CTkCheckBox(
            self.options_frame, 
            text="Include Numbers (0-9)", 
            variable=self.numbers_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            command=self.generate_password,
            checkmark_color="#FFFFFF",
            fg_color="#3B82F6",
            hover_color="#2563EB"
        )
        self.numbers_cb.pack(padx=25, pady=8, anchor="w")
        
        self.symbols_var = ctk.BooleanVar(value=False)
        self.symbols_cb = ctk.CTkCheckBox(
            self.options_frame, 
            text="Include Symbols (!@#$%^&*)", 
            variable=self.symbols_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            command=self.generate_password,
            checkmark_color="#FFFFFF",
            fg_color="#3B82F6",
            hover_color="#2563EB"
        )
        self.symbols_cb.pack(padx=25, pady=(8, 15), anchor="w")
        
        # Display Box for Generated Password (Monospaced font for enhanced readability)
        self.password_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Click Generate to create a password",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            justify="center",
            height=42,
            corner_radius=8,
            border_color=("#D1D5DB", "#4B5563")
        )
        self.password_entry.pack(padx=20, pady=(15, 5), fill="x")
        
        # Strength Meter Section (Dynamic progress indicators)
        self.strength_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.strength_frame.pack(padx=25, pady=5, fill="x")
        
        self.strength_desc_label = ctk.CTkLabel(
            self.strength_frame,
            text="Password Strength:",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#6B7280", "#9CA3AF")
        )
        self.strength_desc_label.pack(side="left")
        
        self.strength_label = ctk.CTkLabel(
            self.strength_frame,
            text="Evaluating...",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#9CA3AF"
        )
        self.strength_label.pack(side="right")
        
        self.strength_bar = ctk.CTkProgressBar(
            self,
            height=6,
            corner_radius=4
        )
        self.strength_bar.set(0.0)
        self.strength_bar.pack(padx=25, pady=(2, 15), fill="x")
        
        # Buttons layout frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(padx=20, pady=(5, 25), fill="x")
        
        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self.buttons_frame, 
            text="🔄 Generate", 
            command=self.generate_password,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=42,
            corner_radius=8
        )
        self.generate_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        # Copy to Clipboard Button
        self.copy_btn = ctk.CTkButton(
            self.buttons_frame, 
            text="📋 Copy", 
            command=self.copy_to_clipboard,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#10B981",  # Vibrant emerald green accent
            hover_color="#059669",
            height=42,
            corner_radius=8
        )
        self.copy_btn.pack(side="right", fill="x", expand=True, padx=(6, 0))
        
        # Auto-generate a password on initial application launch
        self.generate_password()
        
    def update_length_label(self, value):
        """Updates the length label text and triggers a password regeneration."""
        self.length_label.configure(text=f"Password Length: {int(value)}")
        self.generate_password()
        
    def generate_password(self):
        """Generates a random password using the selected sets and length."""
        length = int(self.length_slider.get())
        
        # Assemble custom character pool based on checkbox selections
        char_pool = ""
        if self.uppercase_var.get():
            char_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            char_pool += string.ascii_lowercase
        if self.numbers_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            # Standard safe special characters
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        # Gracefully handle case where no categories are checked
        if not char_pool:
            self.password_entry.delete(0, ctk.END)
            self.password_entry.configure(placeholder_text="Select options above")
            self.strength_label.configure(text="No options selected", text_color="#EF4444")
            self.strength_bar.set(0.0)
            self.strength_bar.configure(progress_color="#EF4444")
            return
            
        # Generate the password
        password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Clear previous content and set the new password
        self.password_entry.delete(0, ctk.END)
        self.password_entry.insert(0, password)
        
        # Update visual strength indicators
        self.update_strength_meter(password)
        
    def update_strength_meter(self, password):
        """Calculates password entropy (bits) and updates strength visuals."""
        if not password:
            self.strength_label.configure(text="None", text_color="#9CA3AF")
            self.strength_bar.set(0.0)
            return

        length = len(password)
        
        # Find sets present in the generated password
        pool_size = 0
        if any(c.isupper() for c in password):
            pool_size += 26
        if any(c.islower() for c in password):
            pool_size += 26
        if any(c.isdigit() for c in password):
            pool_size += 10
            
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            pool_size += len(special_chars)

        if pool_size == 0:
            self.strength_label.configure(text="None", text_color="#9CA3AF")
            self.strength_bar.set(0.0)
            return

        # Calculate bits of entropy (E = L * log2(R))
        entropy = length * math.log2(pool_size)
        
        # Map entropy thresholds to visual color indicators and levels
        if entropy < 35:
            strength_text = "Very Weak"
            color = "#EF4444"  # Crimson Red
            progress = 0.15
        elif entropy < 55:
            strength_text = "Weak"
            color = "#F97316"  # Tangerine Orange
            progress = 0.35
        elif entropy < 75:
            strength_text = "Medium"
            color = "#F59E0B"  # Amber Yellow
            progress = 0.60
        elif entropy < 95:
            strength_text = "Strong"
            color = "#10B981"  # Emerald Green
            progress = 0.85
        else:
            strength_text = "Very Secure"
            color = "#059669"  # Deep Forest Emerald
            progress = 1.0

        # Update labels and progress bar
        self.strength_label.configure(
            text=f"{strength_text} ({int(entropy)} bits)", 
            text_color=color
        )
        self.strength_bar.set(progress)
        self.strength_bar.configure(progress_color=color)
        
    def copy_to_clipboard(self):
        """Copies the generated password to the system clipboard."""
        password = self.password_entry.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()  # Update system clipboard manager
            messagebox.showinfo("Success", "Password copied to clipboard successfully!")
        else:
            messagebox.showwarning("Warning", "No password generated yet. Select at least one option!")

if __name__ == "__main__":
    app = PasswordGeneratorGUI()
    app.mainloop()
