from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import sys
from datetime import datetime

def stitch_videos(file_paths):
    """
    Concatenates videos provided as a list of file paths and saves the merged video.

    Args:
        file_paths (list): List of video file paths to be concatenated.
    """
    if not file_paths:
        raise ValueError("No video file paths provided for stitching.")

    # Load video clips, skipping any that don't exist.
    clips = []
    for path in file_paths:
        if not os.path.exists(path):
            print(f"Warning: File does not exist and will be skipped: {path}")
            continue
        clip = VideoFileClip(path)
        clips.append(clip)

    if not clips:
        raise ValueError("None of the provided video file paths could be loaded.")

    # Concatenate videos
    final_video = concatenate_videoclips(clips)

    # Ensure the output directory exists
    output_dir = "./videos"
    os.makedirs(output_dir, exist_ok=True)

    # Build the output file path using the timestamp
    output_file = os.path.join(output_dir, f"merged_video.mp4")

    # Save the merged video with the generated filename (using fps from the first clip)
    final_video.write_videofile(output_file, codec="libx264", fps=clips[0].fps)

    # Close all video clips to free resources
    for clip in clips:
        clip.close()

if __name__ == "__main__":
    # Command line usage:
    # python stich_videos.py run <video1.mp4> <video2.mp4> ...
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # If no videos are provided, use default ones
        video_files = sys.argv[2:] if len(sys.argv) > 2 else [
            "./videos/test_video.mp4",
            "./videos/video_02.mp4"
        ]
        stitch_videos(video_files)
    else:
        print("Usage: python stich_videos.py run [video1.mp4 video2.mp4 ...]")

