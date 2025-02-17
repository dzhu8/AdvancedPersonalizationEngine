import { Card } from "@/components/ui/card";

const VideoOutput = () => {
  // Check if we're running on localhost
  const isLocalhost = window.location.hostname.includes("localhost");
  
  // Decide the video source based on environment
  const videoSrc = isLocalhost
    ? "http://127.0.0.1:8000/videos/merged_video.mp4"
    : "https://sundai-backend.ryanhughes624.com/videos/merged_video.mp4";
    // ^ Adjust the production URL as needed

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl p-8 glass-effect fade-in">
        <div className="space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-semibold tracking-tight">Your Personalized Ad</h1>
            <p className="text-muted-foreground">
              Here's your customized advertisement
            </p>
          </div>

          <div className="aspect-video bg-black/5 rounded-lg overflow-hidden">
            <video className="w-full h-full" controls>
              <source src={videoSrc} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default VideoOutput;
