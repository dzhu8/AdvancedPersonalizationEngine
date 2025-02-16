import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/use-toast";
// Inside BrandSelection.tsx
import { useAdContext } from "../context/AdContext";


const FileUploadPage = () => {
  const navigate = useNavigate();
  const { selectedFile, setSelectedFile } = useAdContext(); // <-- from Context

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    } else {
      setSelectedFile(null);
    }
  };

  // We'll just navigate next without uploading here:
  const handleNext = (e: React.FormEvent) => {
    e.preventDefault();

    // Basic validation
    if (!selectedFile) {
      toast({
        title: "No file selected",
        description: "Please select a JPEG file",
        variant: "destructive",
      });
      return;
    }

    // Move to brand selection
    navigate("/brand-selection");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl p-8 glass-effect fade-in">
        <div className="space-y-6">
          <div className="space-y-2 text-center">
            <h1 className="text-3xl font-semibold tracking-tight">Ad4You</h1>
            <p className="text-muted-foreground">
              Please upload your JPEG/JPG of your persona
            </p>
          </div>

          <form onSubmit={handleNext} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">
                Upload JPEG
              </label>
              <Input
                type="file"
                accept="image/jpeg, image/jpg"
                onChange={handleFileChange}
                className="bg-white/50 border-2 border-primary/20 
                           focus:border-primary/50 focus:ring-0 
                           transition-all duration-300"
              />
            </div>
            <Button 
              type="submit" 
              disabled={!selectedFile}
              className="w-full h-12 mt-4"
            >
              Next
            </Button>
          </form>

          <div className="text-sm text-center text-muted-foreground">
            <p>Make sure to choose the correct file before proceeding.</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default FileUploadPage;
