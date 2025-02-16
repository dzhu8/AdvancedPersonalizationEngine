import requests
import json
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def generate_storyboard(
        self,
        image_path: str,
        instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete storyboard from an image
        
        Args:
            image_path: Path to the local image file
            instructions: Optional custom instructions
            
        Returns:
            Dict containing analysis and storyboard scenes
        """
        endpoint = f"{self.api_url}/generate-storyboard"
        
        data = {}
        if instructions:
            data['instructions'] = instructions
            
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path.split('/')[-1], f, 'image/png')
            }
            
            response = requests.post(endpoint, data=data, files=files)
            response.raise_for_status()
            return response.json()

# Example usage
if __name__ == "__main__":
    client = APIClient("http://localhost:8000")
    result = client.generate_storyboard("/home/navid/Pictures/Screenshots/IG_profile_example.png")
    print(result) 