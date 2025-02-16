import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";

// Import your AdProvider
import { AdProvider } from "@/context/AdContext";

import InstagramInput from "./pages/InstagramInput";
import BrandSelection from "./pages/BrandSelection";
import VideoOutput from "./pages/VideoOutput";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      {/* Wrap everything inside AdProvider so all children can use it */}
      <AdProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<InstagramInput />} />
            <Route path="/brand-selection" element={<BrandSelection />} />
            <Route path="/video-output" element={<VideoOutput />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </AdProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
