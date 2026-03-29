import os, time, subprocess, csv
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import config

class VideoEngine:
    def __init__(self, log_func):
        self.log = log_func
        self.model = None

    def load_corrections(self):
        """Membaca kamus koreksi dari lib/voc.csv"""
        lib_dir = os.path.join(config.BASE_DIR, "lib")
        csv_path = os.path.join(lib_dir, "voc.csv")
        dict_koreksi = {}

        if not os.path.exists(lib_dir): os.makedirs(lib_dir)

        if not os.path.exists(csv_path):
            try:
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Salah", "Benar"]) 
                    writer.writerow(["AMIR", "AMIN"])
                    writer.writerow(["HALUYA", "HALELUYA"])
                self.log(f"ℹ️ Membuat file baru di: lib/voc.csv")
            except Exception as e:
                self.log(f"⚠️ Gagal membuat file CSV: {e}")
            return {"AMIR": "AMIN"}

        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Salah') and row.get('Benar'):
                        salah = row['Salah'].strip().upper()
                        benar = row['Benar'].strip().upper()
                        dict_koreksi[salah] = benar
            return dict_koreksi
        except Exception as e:
            self.log(f"⚠️ Gagal membaca voc.csv: {e}")
            return {}

    def cut_clip(self, input_path, custom_out=None):
        output_filename = custom_out if custom_out else "step1_cut.mp4"
        out = os.path.join(config.BASE_DIR, "temp", output_filename)
        
        try:
            with VideoFileClip(input_path) as clip:
               
                ts = int(time.time() * 1000)
                temp_audio = os.path.join(config.BASE_DIR, "temp", f"audio_cut_{ts}.m4a")
                clip.write_videofile(
                    out, codec="libx264", audio_codec="aac", fps=30, 
                    logger=None, temp_audiofile=temp_audio, remove_temp=True
                )
            return out
        except Exception as e:
            self.log(f"❌ Gagal Cut: {e}")
            return None

    def run_final_pipeline(self, cut_path):
        try:
            base_name = os.path.basename(cut_path)
            cleaned_path = self.clean_audio(cut_path, base_name)
            if cleaned_path:
                return self.apply_subtitles(cleaned_path, base_name)
        except Exception as e:
            self.log(f"❌ Error Pipeline: {e}")
            return None

    def clean_audio(self, input_path, base_name):
        self.log(f"🔉 Tahap 2: Denoiser {base_name}...")
        
        # 1. Pastikan Path FFmpeg Benar
        ffmpeg_exe = os.path.normpath(os.path.join(config.BASE_DIR, "bin", "ffmpeg.exe"))
        
        # Cek fisik file: Apakah benar-benar ada di sana?
        if not os.path.exists(ffmpeg_exe):
            self.log(f"❌ ERROR: FFmpeg tidak ditemukan di jalur: {ffmpeg_exe}")
            self.log("💡 Pastikan file ffmpeg.exe ada di dalam folder 'bin' di proyek kamu.")
            return None

        out = os.path.join(config.BASE_DIR, "temp", f"clean_{base_name}")
        if os.path.exists(out): 
            try: os.remove(out)
            except: pass

        cmd = [
            ffmpeg_exe, "-y", "-i", input_path,
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-af", "afftdn=nf=-25,loudnorm=I=-14:tp=-1", out
        ]

        try:
            # Gunakan shell=True jika kamu di Windows agar lebih stabil mencari path
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return out
        except subprocess.CalledProcessError as e:
            self.log(f"❌ FFmpeg Error: {e}")
            return None
        except Exception as e:
            self.log(f"❌ Gagal Clean Audio: {e}")
            return None

    def apply_subtitles(self, input_path, base_name):
        self.log(f"✍️ Tahap 3: AI Subtitle (Offline Mode - lib/models/small)...")
        video = None
        final_clip = None
        try:
            # 1. Load Kamus Koreksi dari CSV
            corrections = self.load_corrections()

            
            if not self.model:
                model_path = os.path.join(config.BASE_DIR, "lib", "models", "small")
                
                if not os.path.exists(os.path.join(model_path, "model.bin")):
                    self.log("❌ ERROR: File model.bin tidak ditemukan di folder lib/models/small!")
                    return None

                self.log(f"🧠 Memuat Model AI dari folder lokal...")
                from faster_whisper import WhisperModel
                
                self.model = WhisperModel(
                    model_path, 
                    device="cpu", 
                    compute_type="int8",
                    local_files_only=True 
                )
            
            # 3. Transkripsi Audio
            church_context = "Shalom, Tuhan Yesus Kristus, Haleluya, Amin, Alkitab, Firman Tuhan."
            segments, info = self.model.transcribe(
                input_path, 
                beam_size=5, 
                word_timestamps=True,
                language="id", 
                initial_prompt=church_context, 
                vad_filter=True
            )
            segments = list(segments)

            # 4. Logika Penamaan File (Viral Title)
            full_text = " ".join([seg.text for seg in segments[:1]]).strip()
            clean_title = "".join([c for c in full_text if c.isalnum() or c==' ']).strip()
            viral_title = clean_title[:50] if clean_title else "Untitled_Clip"

            # 5. Olah Video (MoviePy)
            video = VideoFileClip(input_path)
            w, h = video.size
            
            # Auto-Crop 9:16 (Portrait)
            if (w/h) > (9/16): 
                video = video.crop(x_center=w/2, width=h*(9/16))
            
            video = video.resize(height=1280)
            w, h = video.size

            # 6. Generate Subtitle per Kata
            subtitle_clips = []
            for segment in segments:
                for word in segment.words:
                    raw_word = word.word.strip().upper()
                    
                    # Terapkan koreksi dari voc.csv
                    clean_text = corrections.get(raw_word, raw_word)
                    if not clean_text: continue
                    
                    duration = word.end - word.start
                    if duration <= 0: duration = 0.1
                    
                    # Style Subtitle: Kuning, Arial Bold, Stroke Hitam
                    word_clip = TextClip(
                        clean_text, fontsize=90, color='yellow', font='Arial-Bold',
                        stroke_color='black', stroke_width=2.5, method='label'
                    ).set_start(word.start).set_duration(duration).set_position(('center', h * 0.6))
                    
                    subtitle_clips.append(word_clip)

            # 7. Penggabungan & Render Akhir
            final_clip = CompositeVideoClip([video] + subtitle_clips)
            out_final = os.path.join(config.BASE_DIR, "outputs", f"{viral_title}.mp4")
            
            # Solusi WinError 32: Nama audio unik dengan milidetik
            ts = int(time.time() * 1000)
            temp_audio_final = os.path.join(config.BASE_DIR, "temp", f"audio_final_{ts}.m4a")
            
            final_clip.write_videofile(
                out_final, 
                codec="libx264", 
                audio_codec="aac", 
                fps=30, 
                logger=None, 
                temp_audiofile=temp_audio_final, 
                remove_temp=True
            )
            
            self.log(f"🎉 SELESAI: {viral_title}")
            return out_final

        except Exception as e:
            self.log(f"❌ Gagal Subtitle: {e}")
            return None
        finally:
            # Tutup semua file agar tidak terkunci (WinError 32 prevention)
            if video: video.close()
            if final_clip: final_clip.close()