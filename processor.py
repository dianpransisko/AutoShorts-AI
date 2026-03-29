import os, time
import config
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from faster_whisper import WhisperModel

class FullProcessor:
    def __init__(self, log_func):
        self.log = log_func
        self.model = None

    def run_clean_audio(self, input_path):
        try:
            self.log("🔉 Tahap 2: Membersihkan Audio...")
            output_clean = os.path.join(config.BASE_DIR, "temp", "step2_clean.mp4")
            video = VideoFileClip(input_path)
            video.write_videofile(
                output_clean, codec="libx264",
                ffmpeg_params=["-af", "afftdn=nf=-25,loudnorm=I=-14:LRA=7:tp=-1", "-c:a", "aac"],
                logger=None
            )
            video.close()
            self.log("✅ Tahap 2 Selesai! Suara -14 LUFS.")
            return output_clean
        except Exception as e:
            self.log(f"❌ Error Tahap 2: {e}")
            return None

    def run_subtitle(self, input_path):
        try:
            if not self.model:
                self.log("🧠 Memuat AI Whisper...")
                self.model = WhisperModel("base", device="cpu", compute_type="int8", 
                                          download_root=os.path.join(config.BASE_DIR, "models"))
            
            self.log("✍️ Tahap 3: AI sedang bekerja...")
            segments, _ = self.model.transcribe(input_path, word_timestamps=True, language="id")
            
            video = VideoFileClip(input_path)
            w, h = video.size
            all_clips = [video]

            for segment in segments:
                for word in segment.words:
                    txt = TextClip(word.word.strip().upper(), fontsize=75, color='yellow', font='Arial-Bold',
                                  stroke_color='black', stroke_width=2, method='caption', 
                                  size=(w*0.8, None)).set_start(word.start).set_end(min(word.end, video.duration)).set_position(('center', h*0.75))
                    all_clips.append(txt)

            out_name = f"Final_Shorts_{int(time.time())}.mp4"
            final_path = os.path.join(config.BASE_DIR, "outputs", out_name)
            
            final_v = CompositeVideoClip(all_clips, size=(w, h))
            final_v.set_duration(video.duration).set_audio(video.audio).write_videofile(final_path, codec="libx264", fps=24, logger=None)
            
            video.close()
            final_v.close()
            self.log(f"🎉 SELESAI! File: {out_name}")
        except Exception as e:
            self.log(f"❌ Error Tahap 3: {e}")