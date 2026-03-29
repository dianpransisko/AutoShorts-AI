import os, threading, time, config, subprocess
import customtkinter as ctk
from tkinter import filedialog
from obs_manager import OBSManager
from video_logic import VideoEngine
from ui_components import ProgressPopup
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HUGGINGFACE_HUB_TOKEN"] = ""


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoShorts AI - Modular Suite")
        self.geometry("700x850")
        ctk.set_appearance_mode("dark")
        
        self.obs = OBSManager()
        self.engine = VideoEngine(self.write_log)
        
        self.is_monitoring = False
        self.selected_files = [] 
        self.checkbox_vars = {}  

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        self.check_initial_state()

    def check_initial_state(self):
        env = config.get_env_data()
        if not env["OBS_PASS"] or not os.path.exists(env["WATCH_DIR"]):
            self.show_setup_screen(env)
        else:
            self.show_dashboard_screen()

    # ================= LAYAR SETUP =================
    def show_setup_screen(self, env):
        for w in self.container.winfo_children(): w.destroy()
        frame = ctk.CTkFrame(self.container, corner_radius=15)
        frame.pack(padx=50, pady=30, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="⚙️ Konfigurasi Sistem", font=("Arial", 24, "bold")).pack(pady=15)
        
        self.ent_host = self.create_input(frame, "OBS Host:", env["OBS_HOST"])
        self.ent_port = self.create_input(frame, "OBS Port:", env["OBS_PORT"])
        self.ent_pass = self.create_input(frame, "OBS Pass:", env["OBS_PASS"], is_pwd=True)
        self.ent_magick = self.create_input(frame, "Magick.exe:", env["IMAGEMAGICK_PATH"], browse=True, is_file=True)
        self.ent_watch = self.create_input(frame, "Watch Dir:", env["WATCH_DIR"], browse=True, is_file=False)
        
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="#e74c3c")
        self.lbl_error.pack(pady=5)
        ctk.CTkButton(frame, text="VERIFIKASI & SIMPAN", fg_color="#2ecc71", height=45, command=self.start_validation).pack(pady=20)

    def create_input(self, parent, label, default, is_pwd=False, browse=False, is_file=False):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(pady=5, fill="x", padx=40)
        ctk.CTkLabel(row, text=label, width=100, anchor="w").pack(side="left")
        e = ctk.CTkEntry(row, show="*" if is_pwd else "")
        e.insert(0, default)
        e.pack(side="left", expand=True, fill="x", padx=(0, 5))
        if browse:
            ctk.CTkButton(row, text="🔍", width=40, command=lambda: self.browse_path(e, is_file)).pack(side="right")
        return e

    def browse_path(self, entry, is_file):
        path = filedialog.askopenfilename() if is_file else filedialog.askdirectory()
        if path:
            entry.delete(0, "end")
            entry.insert(0, os.path.normpath(path))

    def start_validation(self):
        threading.Thread(target=self.validate_and_save, daemon=True).start()

    def validate_and_save(self):
        h, p, pwd = self.ent_host.get(), self.ent_port.get(), self.ent_pass.get()
        m, w = self.ent_magick.get(), self.ent_watch.get()
        try:
            self.obs.connect(h, p, pwd)
            config.save_env_data(h, p, pwd, m, w)
            self.after(0, self.show_dashboard_screen)
        except Exception as e:
            self.after(0, lambda: self.lbl_error.configure(text=f"Gagal: {str(e)}"))

    # ================= LAYAR DASHBOARD =================
    def show_dashboard_screen(self):
        for w in self.container.winfo_children(): w.destroy()
        frame = ctk.CTkFrame(self.container, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="🎬 Video Pipeline Dashboard", font=("Arial", 22, "bold")).pack(pady=10)
        self.log_box = ctk.CTkTextbox(frame, width=600, height=250)
        self.log_box.pack(pady=10)
        
        self.btn_monitor = ctk.CTkButton(frame, text="🟢 MULAI REKAM KLIP", fg_color="#2ecc71", command=self.toggle_record)
        self.btn_monitor.pack(pady=5)

        ctk.CTkLabel(frame, text="📁 Pilih Video untuk Diproses:", font=("Arial", 11, "bold")).pack(pady=(10,0))
        self.scroll_frame = ctk.CTkScrollableFrame(frame, width=500, height=180)
        self.scroll_frame.pack(pady=5, padx=50, fill="x")
        
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(pady=10)
        
        self.b1 = ctk.CTkButton(grid, text="1. BATCH CUT", width=180, state="disabled", command=self.do_batch_cut)
        self.b1.grid(row=0, column=0, padx=10)
        
        self.b2 = ctk.CTkButton(grid, text="2. BATCH FINAL", width=180, state="disabled", fg_color="#9b59b6", command=self.do_batch_final)
        self.b2.grid(row=0, column=1, padx=10)

        self.btn_clean = ctk.CTkButton(frame, text="🗑️ BERSIHKAN FOLDER TEMP", fg_color="#34495e", hover_color="#c0392b", command=self.run_cleanup_script)
        self.btn_clean.pack(pady=10)

        ctk.CTkButton(frame, text="⚙️ CONFIG", fg_color="#34495e", command=lambda: self.show_setup_screen(config.get_env_data())).pack(side="bottom", pady=10)
        self.refresh_file_list()

    # ================= LOGIKA SISTEM =================
    def set_all_buttons_state(self, state):
        """Mencegah klik tombol saat proses berjalan"""
        self.btn_monitor.configure(state=state)
        self.b1.configure(state=state)
        self.b2.configure(state=state)
        self.btn_clean.configure(state=state)

    def run_cleanup_script(self):
        bat_path = os.path.join(config.BASE_DIR, "del.bat") 
        if os.path.exists(bat_path):
            try:
                subprocess.Popen([bat_path], shell=True)
                self.write_log("🧹 Proses pembersihan video lama...")
                self.latest_cut = None
                self.b2.configure(state="disabled")
            except Exception as e:
                self.write_log(f"❌ Gagal: {e}")
        else:
            self.write_log("⚠️ File 'del.bat' tidak ditemukan.")

    def refresh_file_list(self):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        self.checkbox_vars = {}
        env = config.get_env_data()
        watch_dir = env["WATCH_DIR"]
        if os.path.exists(watch_dir):
            files = [f for f in os.listdir(watch_dir) if f.endswith(".mp4")]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(watch_dir, x)), reverse=True)
            for f in files:
                var = ctk.StringVar(value="off")
                cb = ctk.CTkCheckBox(self.scroll_frame, text=f, variable=var, onvalue=f, offvalue="off", command=self.update_selection)
                cb.pack(anchor="w", pady=2, padx=10)
                self.checkbox_vars[f] = var
        self.update_selection()

    def update_selection(self):
        self.selected_files = [var.get() for var in self.checkbox_vars.values() if var.get() != "off"]
        count = len(self.selected_files)
        st = "normal" if count > 0 else "disabled"
        self.b1.configure(state=st, text=f"1. BATCH CUT ({count})" if count > 0 else "1. BATCH CUT")
        self.b2.configure(state=st, text=f"2. BATCH FINAL ({count})" if count > 0 else "2. BATCH FINAL")

    def write_log(self, msg):
        if hasattr(self, 'log_box'):
            self.after(0, lambda: (self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n"), self.log_box.see("end")))

    def toggle_record(self):
        if not self.is_monitoring: self.start_manual_record()
        else: self.stop_manual_record()

    def start_manual_record(self):
        env = config.get_env_data()
        try:
            self.obs.connect(env["OBS_HOST"], env["OBS_PORT"], env["OBS_PASS"])
            self.obs.start_clip()
            self.is_monitoring = True
            self.btn_monitor.configure(text="🛑 STOP REKAM", fg_color="#e74c3c")
            threading.Thread(target=self.folder_listener, daemon=True).start()
        except Exception as e: self.write_log(f"❌ Error: {e}")

    def stop_manual_record(self):
        self.obs.stop_clip()
        self.is_monitoring = False
        self.btn_monitor.configure(text="🟢 MULAI REKAM KLIP", fg_color="#2ecc71")
        self.after(2000, self.refresh_file_list)

    def folder_listener(self):
        watch_dir = config.get_env_data()["WATCH_DIR"]
        last_count = len(os.listdir(watch_dir))
        while self.is_monitoring:
            time.sleep(2)
            if len(os.listdir(watch_dir)) != last_count:
                self.after(0, self.refresh_file_list)
                last_count = len(os.listdir(watch_dir))

    # --- EKSEKUSI BATCH ---
    def do_batch_cut(self):
        if not self.selected_files: return

        # 1. Kunci tombol LANGSUNG sebelum thread mulai
        self.set_all_buttons_state("disabled")

        def task():
            total_files = len(self.selected_files)
            # Pastikan popup muncul di thread utama lewat after
            popup = ProgressPopup(self, "Batch Cutting", total_files)
            watch_dir = config.get_env_data()["WATCH_DIR"]
            
            for i, filename in enumerate(self.selected_files):
                # Hitung progres
                i_factor = i / total_files
                step_size = 1 / total_files
                
                # --- FIX LAMBDA BINDING ---
                # Kita masukkan variabel ke dalam argumen default lambda (f=i_factor, n=filename)
                # agar nilainya tidak tertukar dengan file berikutnya
                msg_prep = f"PREPARING: {filename[:25]}"
                self.after(0, lambda f=i_factor, s=step_size, m=msg_prep: popup.set_progress(f + (s * 0.1), m))
                
                full_path = os.path.join(watch_dir, filename)
                
                # Eksekusi pemotongan
                # Pastikan di video_logic.py sudah pakai temp_audiofile unik (pake timestamp)
                self.engine.cut_clip(full_path, custom_out=f"cut_{filename}")
                
                # Update Selesai 1 file
                msg_done = f"CUT FINISHED: {filename[:25]}"
                self.after(0, lambda f=i_factor, s=step_size, m=msg_done: popup.set_progress(f + s, m))
            
            # Selesai semua
            self.after(500, popup.destroy)
            self.after(500, lambda: self.set_all_buttons_state("normal"))
            self.write_log("✅ Batch Cut Selesai.")

        # Jalankan di background
        threading.Thread(target=task, daemon=True).start()



    def do_batch_final(self):
        if not self.selected_files: return

        def task():
            self.after(0, lambda: self.set_all_buttons_state("disabled"))
            total_files = len(self.selected_files)
            popup = ProgressPopup(self, "AI Batch Processing", total_files)
            
            temp_dir = os.path.join(config.BASE_DIR, "temp")
            
            for i, filename in enumerate(self.selected_files):
                # i_factor adalah titik awal progres untuk file ke-i
                # Misal ada 2 file: File 1 mulai dari 0.0, File 2 mulai dari 0.5
                i_factor = i / total_files
                step_size = 1 / total_files # Lebar progres untuk 1 file

                target_cut = os.path.join(temp_dir, f"cut_{filename}")
                
                if os.path.exists(target_cut):
                    # TAHAP A: Dimulai (+10% dari jatah file ini)
                    self.after(0, lambda: popup.set_progress(i_factor + (step_size * 0.1), f"CLEANING AUDIO: {filename}"))
                    cleaned_path = self.engine.clean_audio(target_cut, filename)
                    
                    # TAHAP B: AI Transcribe (+50% dari jatah file ini)
                    self.after(0, lambda: popup.set_progress(i_factor + (step_size * 0.5), f"AI SUBTITLING: {filename}"))
                    if cleaned_path:
                        self.engine.apply_subtitles(cleaned_path, filename)
                    
                    # TAHAP C: Selesai 1 file (+100% dari jatah file ini)
                    self.after(0, lambda: popup.set_progress(i_factor + step_size, f"FINISHED: {filename}"))
                else:
                    self.write_log(f"⚠️ Skip: {filename} belum di-CUT.")

            self.write_log("🎉 SEMUA ANTREAN SELESAI!")
            self.after(500, popup.destroy)
            self.after(500, lambda: self.set_all_buttons_state("normal"))
            
            # Buka folder
            os.startfile(os.path.join(config.BASE_DIR, "outputs"))

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    App().mainloop()