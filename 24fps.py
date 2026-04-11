from moviepy.editor import VideoFileClip

input_path = "C:/Users/vamsh/OneDrive/Desktop/video_cloning/video_cloning/videofile.mp4"
output_path = "output_24fps.mp4"

clip = VideoFileClip(input_path)
clip_24 = clip.set_fps(24)
clip_24.write_videofile(
    output_path,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
