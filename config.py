import os
import sys
from moviepy.config import change_settings


# --- 1. LOGIKA PATH DINAMIS ---
if getattr(sys, 'frozen', False):
    # Jika aplikasi berjalan sebagai .exe (setelah dibungkus PyInstaller)
    # BASE_DIR akan menunjuk ke folder tempat AutoShortsAI.exe berada
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Jika masih berjalan sebagai script .py biasa (saat koding)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jalur file .env
ENV_PATH = os.path.join(BASE_DIR, ".env")

# --- 2. PASTIKAN FOLDER KERJA ADA ---
# Tambahkan ini agar folder temp dan outputs otomatis terbuat di lokasi yang benar
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 2. FUNGSI BACA .ENV ---
def get_env_data():
    """Membaca data dari file .env atau memberikan nilai default."""
    
    # Deteksi lokasi folder ImageMagick internal hasil bundling
    local_magick = os.path.join(BASE_DIR, "imagemagick", "magick.exe")
    
    data = {
        "OBS_HOST": "localhost",
        "OBS_PORT": "4455",
        "OBS_PASS": "",
        # Gunakan local_magick sebagai default, jika tidak ada baru ke jalur standar
        "IMAGEMAGICK_PATH": local_magick if os.path.exists(local_magick) else r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
        "WATCH_DIR": os.path.join(os.path.expanduser("~"), "Videos")
    }
    
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    # Menghindari error jika ada tanda '=' di dalam password
                    key, value = line.strip().split("=", 1)
                    data[key] = value
    return data

# --- 3. FUNGSI SIMPAN .ENV ---
def save_env_data(host, port, pwd, magick, watch):
    """Menyimpan konfigurasi user ke file .env secara permanen."""
    with open(ENV_PATH, "w") as f:
        f.write(f"OBS_HOST={host}\n")
        f.write(f"OBS_PORT={port}\n")
        f.write(f"OBS_PASS={pwd}\n")
        f.write(f"IMAGEMAGICK_PATH={magick}\n")
        f.write(f"WATCH_DIR={watch}\n")

# --- 4. INISIALISASI SISTEM ---
# Pastikan folder-folder kerja sudah tercipta otomatis
for folder in ["temp", "outputs", "models", "bin"]:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Ambil data terbaru untuk konfigurasi MoviePy
env = get_env_data()

# Konfigurasi ImageMagick (Hanya jika path-nya benar)
if os.path.exists(env["IMAGEMAGICK_PATH"]):
    change_settings({"IMAGEMAGICK_BINARY": env["IMAGEMAGICK_PATH"]})

# Konfigurasi FFmpeg (Menggunakan ffmpeg.exe yang ada di folder bin)
FFMPEG_EXE = os.path.join(BASE_DIR, "bin", "ffmpeg.exe")
if os.path.exists(FFMPEG_EXE):
    change_settings({"FFMPEG_BINARY": FFMPEG_EXE})