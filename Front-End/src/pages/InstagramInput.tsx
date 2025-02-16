
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/use-toast";

const InstagramInput = () => {
  const [instagramUrl, setInstagramUrl] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!instagramUrl.includes("instagram.com/")) {
      toast({
        title: "Invalid Instagram URL",
        description: "Please enter a valid Instagram profile URL",
        variant: "destructive",
      });
      return;
    }

    navigate("/brand-selection");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl p-8 glass-effect fade-in">
        <div className="space-y-6">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-semibold tracking-tight">Ad4You</h1>
            <p className="text-muted-foreground">Enter an Instagram profile URL to get started</p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <Input
                type="text"
                placeholder="https://instagram.com/username"
                value={instagramUrl}
                onChange={(e) => setInstagramUrl(e.target.value)}
                className="w-full h-12 pl-4 pr-12 text-lg bg-white/50 border-2 border-primary/20 focus:border-primary/50 focus:ring-0 transition-all duration-300"
              />
              <Button 
                type="submit"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 hover-scale"
              >
                Next
              </Button>
            </div>
          </form>
          
          <div className="text-sm text-center text-muted-foreground">
            <p className="font-medium">Important:</p>
            <p>The Instagram profile must be set to private for optimal results</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default InstagramInput;
