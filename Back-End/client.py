import requests
from typing import Optional, Dict, Any

def generate_storyboard_from_image(
    api_url: str,
    image_path: str,
    instructions: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simple example of how to generate a storyboard from an image using the API
    
    Args:
        api_url: Base URL of the API (e.g., 'http://localhost:8000')
        image_path: Path to the local image file
        instructions: Optional custom instructions for analysis
        
    Returns:
        Dict containing:
            - initial_analysis: Raw analysis of the image
            - scenes: Structured storyboard scenes
            
    Example:
        result = generate_storyboard_from_image(
            'http://localhost:8000',
            'path/to/image.jpg',
            'Optional custom instructions'
        )
        
        # Access the results
        analysis = result['initial_analysis']
        scenes = result['scenes']
    """
    endpoint = f"{api_url}/generate-storyboard"
    
    # Prepare the form data
    data = {}
    if instructions:
        data['instructions'] = instructions
        
    # Upload the image
    with open(image_path, 'rb') as f:
        files = {
            'file': (image_path.split('/')[-1], f, 'image/png')
        }
        
        # Make the request
        response = requests.post(endpoint, data=data, files=files)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        return response.json()

# Example usage
if __name__ == "__main__":
    # Example of how to use the API
    try:
        result = generate_storyboard_from_image(
            api_url="http://localhost:8000",
            image_path="/Users/danielrapoport/Desktop/Sundai Practice/AdvancedPersonalizationEngine/Back-End/pictures/IG_profile_example.png"
        )
        
        print("\nResult:")
        print(result)
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
    except KeyError as e:
        print(f"Unexpected response format: {e}") 