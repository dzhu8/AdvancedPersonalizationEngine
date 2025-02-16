// src/context/AdContext.tsx
import React, { createContext, useContext, useState } from "react";

interface AdContextProps {
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  selectedBrand: string | null;
  setSelectedBrand: (brand: string | null) => void;
}

const AdContext = createContext<AdContextProps>({
  selectedFile: null,
  setSelectedFile: () => {},
  selectedBrand: null,
  setSelectedBrand: () => {},
});

export const AdProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);

  return (
    <AdContext.Provider
      value={{ selectedFile, setSelectedFile, selectedBrand, setSelectedBrand }}
    >
      {children}
    </AdContext.Provider>
  );
};

export function useAdContext() {
  return useContext(AdContext);
}
