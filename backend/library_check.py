import subprocess


ffmpeg_path = r"D:\ffmpeg lib\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffmpeg.exe"
ffprobe_path = r"D:\ffmpeg lib\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffprobe.exe"

video_path = r"C:\Users\hoang\Videos\Captures\Honkai_ Star Rail 2025-09-30 15-22-26.mp4"

cmd = [ffprobe_path, "-v", "error", "-show_format", "-show_streams", video_path]
subprocess.run(cmd, check=True)