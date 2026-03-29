import customtkinter as ctk

class ProgressPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, total_steps):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x220")
        
        # Tema & Transparansi
        self.attributes("-topmost", True)
        self.grab_set() 
        self.resizable(False, False)
        self.configure(fg_color="#1a1a1a") # Background Gelap Premium

        # 1. Judul Aksi (Neon Style)
        self.label = ctk.CTkLabel(
            self, 
            text="AI ENGINE INITIALIZING...", 
            font=("Segoe UI", 16, "bold"),
            text_color="#00f2ff" # Cyan Neon
        )
        self.label.pack(pady=(30, 5))

        # 2. Progress Bar (Glow Design)
        # Warna progress bar dibuat Teal/Cyan agar kontras
        self.progress = ctk.CTkProgressBar(
            self, 
            width=350, 
            height=12,
            corner_radius=10,
            progress_color="#1fdbb8", # Teal Electric
            fg_color="#333333"        # Background Bar Kelam
        )
        self.progress.set(0)
        self.progress.pack(pady=15)

        # 3. Label Persentase & Status
        self.percentage_label = ctk.CTkLabel(
            self, 
            text="0%", 
            font=("Consolas", 22, "bold"),
            text_color="#ffffff"
        )
        self.percentage_label.pack()

        self.status_label = ctk.CTkLabel(
            self, 
            text="Waiting for queue...", 
            font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.status_label.pack(pady=(5, 10))
        
        self.total_steps = total_steps


    def set_progress(self, percentage, text):
        """Update persentase secara manual (0.0 sampai 1.0)"""
        self.progress.set(percentage)
        percent_text = int(percentage * 100)
        self.percentage_label.configure(text=f"{percent_text}%")
        
        display_text = text if len(text) < 40 else text[:37] + "..."
        self.label.configure(text=display_text.upper())
        self.update()

        
    def update_step(self, current_step, text):
        """Update tampilan dengan efek animasi teks"""
        if self.total_steps > 0:
            val = current_step / self.total_steps
            self.progress.set(val)
            
            # Hitung persentase
            percent = int(val * 100)
            self.percentage_label.configure(text=f"{percent}%")
        
        # Potong teks jika kepanjangan agar tidak merusak layout
        display_text = text if len(text) < 40 else text[:37] + "..."
        
        self.label.configure(text=display_text.upper())
        self.status_label.configure(text=f"Batch Task: {current_step} of {self.total_steps} Processing")
        
        # Maksa Windows untuk nge-refresh UI saat itu juga
        self.update()