
import { Card } from "@/components/ui/card";

const VideoOutput = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl p-8 glass-effect fade-in">
        <div className="space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-semibold tracking-tight">Your Personalized Ad</h1>
            <p className="text-muted-foreground">Here's your customized advertisement</p>
          </div>

          <div className="aspect-video bg-black/5 rounded-lg overflow-hidden">
            <div className="w-full h-full flex items-center justify-center">
              <p className="text-muted-foreground">Video Output Placeholder</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default VideoOutput;
