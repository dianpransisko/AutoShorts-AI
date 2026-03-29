from moviepy.editor import VideoFileClip
import os
import config

def run_cut(input_path, log_func):
    try:
        log_func(f"✂️ Tahap 1: Memotong video...")
        output_cut = os.path.join(config.BASE_DIR, "temp", "step1_cut.mp4")
        
        video = VideoFileClip(input_path)
        start_t = max(0, video.duration - 60) # Ambil 60 detik terakhir
        
        video.subclip(start_t, video.duration).write_videofile(output_cut, codec="libx264", logger=None)
        video.close()
        log_func("✅ Tahap 1 Selesai! File tersimpan di temp.")
        return output_cut
    except Exception as e:
        log_func(f"❌ Error Tahap 1: {e}")
        return None