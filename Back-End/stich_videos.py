#from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy

# Load video clips
video1 = moviepy.VideoFileClip("./videos/test_video.mp4")
video2 = moviepy.VideoFileClip("./videos/video_02.mp4")

# Concatenate videos
final_video = moviepy.concatenate_videoclips([video1, video2])

# Save the merged video
final_video.write_videofile("./videos/merged_video.mp4", codec="libx264", fps=video1.fps)
