#from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy
from datetime import datetime

# Load video clips
video1 = moviepy.VideoFileClip("./videos/test_video.mp4")
video2 = moviepy.VideoFileClip("./videos/video_02.mp4")

# Concatenate videos
final_video = moviepy.concatenate_videoclips([video1, video2])

# Save the merged video
output_dir = "./videos"
# Generate a timestamp (YYYYMMDD_HHMMSS)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Build the output file path using the timestamp
output_file = os.path.join(output_dir, f"merged_video_{timestamp}.mp4")

# Save the merged video with the generated filename
final_video.write_videofile(output_file, codec="libx264", fps=video1.fps)
