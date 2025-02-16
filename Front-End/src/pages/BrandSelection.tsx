import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/use-toast";
import { useAdContext } from "../context/AdContext";

const BRANDS = [
  {
    id: "coca-cola",
    name: "Coca Cola",
    logo: "/lovable-uploads/d5abb83f-5029-427a-ac95-a8b1a6dbedc1.png",
  },
  {
    id: "wip",
    name: "Work in Progress",
    logo: "/placeholder.svg",
    disabled: true,
  },
];

const BrandSelection = () => {
  const navigate = useNavigate();
  const { selectedFile, selectedBrand, setSelectedBrand } = useAdContext();

  const handleBrandSelect = (brandId: string) => {
    setSelectedBrand(brandId);
    console.log("Selected brand:", brandId);
  };

  const handleNext = async () => {
    if (!selectedFile) {
      toast({
        title: "No file uploaded",
        description: "Please go back and upload a file first.",
        variant: "destructive",
      });
      return;
    }

    if (!selectedBrand) {
      toast({
        title: "No brand selected",
        description: "Please select a brand before continuing.",
        variant: "destructive",
      });
      return;
    }

    // Detect if we're on localhost
    const isLocalhost = window.location.hostname.includes("localhost");
    // If true, point to local Uvicorn server, else production.
    const uploadUrl = isLocalhost
      ? "http://127.0.0.1:8000/process-screenshot"
      : "https://sundai-backend.ryanhughes624.com/process-screenshot";

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("brand", selectedBrand);

      console.log("Sending to:", uploadUrl);
      console.log("File:", selectedFile);
      console.log("Brand:", selectedBrand);

      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("Server error response:", errorData);
        toast({
          title: "Upload failed",
          description: errorData?.message || "Something went wrong on the server.",
          variant: "destructive",
        });
        return;
      }

      toast({
        title: "Success!",
        description: "Your brand and file have been uploaded.",
      });

      navigate("/video-output");
    } catch (error) {
      console.error("Upload error:", error);
      toast({
        title: "Error",
        description: "Unable to upload. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl p-8 glass-effect fade-in">
        <div className="space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-semibold tracking-tight">Select a Brand</h1>
            <p className="text-muted-foreground">Choose the brand you want to create an ad for</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {BRANDS.map((brand) => (
              <button
                key={brand.id}
                disabled={brand.disabled}
                onClick={() => !brand.disabled && handleBrandSelect(brand.id)}
                className={`
                  relative p-6 rounded-lg hover-scale
                  ${brand.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                  ${
                    selectedBrand === brand.id
                      ? 'ring-2 ring-primary shadow-lg'
                      : 'bg-white/50'
                  }
                  transition-all duration-300 ease-in-out
                `}
              >
                <div className="aspect-video flex items-center justify-center">
                  <img
                    src={brand.logo}
                    alt={brand.name}
                    className="max-h-24 object-contain"
                  />
                </div>
                <p className="mt-4 text-lg font-medium text-center">{brand.name}</p>
              </button>
            ))}
          </div>

          <div className="flex justify-center">
            <Button
              onClick={handleNext}
              disabled={!selectedBrand}
              className="px-8 py-6 text-lg hover-scale"
            >
              Next
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default BrandSelection;
