import instaloader
import os

# Define your Instagram username
USERNAME = "advancedpersonalizationengine"  # Replace with your actual Instagram username
SESSION_FILE = "C:/Users/linnb/AppData/Local/Instaloader/session-advancedpersonalizationengine."  # Change if needed
# Initialize Instaloader instance
L = instaloader.Instaloader(download_videos=False, download_pictures=True, save_metadata=False)

# Try to load an existing session
if os.path.exists(SESSION_FILE):
    try:
        L.load_session_from_file(USERNAME, SESSION_FILE)
        print("✅ Logged in using saved session.")
    except Exception as e:
        print(f"⚠️ Failed to load session: {e}")
        os.remove(SESSION_FILE)  # Remove invalid session
        L.login(USERNAME, input("Enter Instagram password: "))  # Prompt for login
        L.save_session_to_file(SESSION_FILE)  # Save session for future use
else:
    # If no session is found, log in and save it
    L.login(USERNAME, input("Enter Instagram password: "))
    L.save_session_to_file(SESSION_FILE)
    print(f"✅ New session saved to {SESSION_FILE}.")

# Ask user for a profile to fetch images from
profile_name = input("Enter Instagram profile username to load: ")

try:
    # Fetch profile data
    profile = instaloader.Profile.from_username(L.context, profile_name)

    # Create directory for profile downloads
    profile_folder = f"./{profile.username}"
    os.makedirs(profile_folder, exist_ok=True)

    # **Download Latest Posts (Only Images)**
    post_limit = 5  # Adjust the number of posts to download
    images = []
    captions = []

    print(f"📥 Downloading latest {post_limit} image posts...")
    for i, post in enumerate(profile.get_posts()):
        if i >= post_limit:
            break
        if post.is_video:  # Skip videos
            continue
        
        L.download_post(post, target=profile.username)
        print(f"✅ Downloaded image post {i+1}")

        # Find the downloaded image file (skipping metadata and videos)
        for file in os.listdir(profile_folder):
            if file.endswith(".jpg") and file.startswith(post.date_utc.strftime("%Y-%m-%d")):
                images.append(os.path.join(profile_folder, file))
                captions.append(post.caption if post.caption else "No Caption")
                break

    # **Merge All Images into One Large JPEG**
    if images:
        print("🖼️ Merging images into one large JPEG...")
        image_list = [Image.open(img) for img in images]
        total_width = max(img.width for img in image_list)
        total_height = sum(img.height for img in image_list)
        
        merged_image = Image.new("RGB", (total_width, total_height))
        
        y_offset = 0
        for img in image_list:
            merged_image.paste(img, (0, y_offset))
            y_offset += img.height
        
        merged_image.save(os.path.join(profile_folder, "merged_image.jpg"))
        print(f"✅ Merged image saved at {profile_folder}/merged_image.jpg")

    # **Save Aggregated Captions**
    captions_text = "\n\n---\n\n".join(captions)
    with open(os.path.join(profile_folder, "captions.txt"), "w", encoding="utf-8") as f:
        f.write(captions_text)
    print(f"✅ Captions saved at {profile_folder}/captions.txt")

except instaloader.exceptions.ProfileNotExistsException:
    print("❌ Profile does not exist.")
except instaloader.exceptions.ConnectionException:
    print("❌ Could not connect to Instagram. Check your internet or session.")
except Exception as e:
    print(f"⚠️ Error: {e}")
