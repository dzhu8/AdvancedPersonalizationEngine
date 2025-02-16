
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleNext = () => {
    if (selectedBrand) {
      navigate("/video-output");
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
                onClick={() => !brand.disabled && setSelectedBrand(brand.id)}
                disabled={brand.disabled}
                className={`
                  relative p-6 rounded-lg hover-scale
                  ${brand.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                  ${selectedBrand === brand.id ? 'ring-2 ring-primary shadow-lg' : 'bg-white/50'}
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
