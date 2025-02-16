import requests
import json
from typing import Optional, Dict, Any

def process_file_url(api_url: str, file_url: str, instructions: str = None):
    """
    Send a file URL (image or PDF) to the API for processing
    
    Args:
        api_url: The base URL of the API (e.g., 'http://localhost:8000')
        file_url: URL of the file to analyze
        instructions: Optional instructions for analysis
    """
    # Prepare the endpoint URL
    endpoint = f"{api_url}/process-screenshot"
    
    # Prepare the form data
    data = {
        'file_url': file_url  # Changed from image_url to file_url to match app.py
    }
    
    # Add instructions if provided
    if instructions:
        data['brand_instructions'] = instructions
    
    try:
        # Make the POST request
        response = requests.post(endpoint, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Print the raw response for debugging
        print("Raw Response:", response.text)
        
        # Parse the JSON response
        result = response.json()
        
        # Check if there's an error in the response
        if 'error' in result:
            print("Error from server:", result['error'])
            return result
            
        # Print the analysis if available
        if 'analysis' in result:
            print("Analysis Result:", result['analysis'])
            
            if 'brand_instructions' in result:
                print("Used Instructions:", result['brand_instructions'])
        else:
            print("No analysis found in response")
            print("Full response:", result)
            
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", response.text)
        return None

def process_local_file(api_url: str, file_path: str, instructions: str = None):
    """
    Send a local file (image or PDF) to the API for processing
    
    Args:
        api_url: The base URL of the API (e.g., 'http://localhost:8000')
        file_path: Path to the local file
        instructions: Optional instructions for analysis
    """
    # Prepare the endpoint URL
    endpoint = f"{api_url}/process-screenshot"
    
    # Prepare the form data
    data = {}
    if instructions:
        data['brand_instructions'] = instructions
    
    # Open and attach the file
    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path.split('/')[-1], f, 'image/png')  # Assuming PNG, adjust if needed
        }
        
        try:
            # Make the POST request with the file
            response = requests.post(endpoint, data=data, files=files)
            response.raise_for_status()
            
            # Print the raw response for debugging
            print("Raw Response:", response.text)
            
            # Parse the JSON response
            result = response.json()
            
            # Check if there's an error in the response
            if 'error' in result:
                print("Error from server:", result['error'])
                return result
                
            # Print the analysis if available
            if 'analysis' in result:
                print("Analysis Result:", result['analysis'])
                
                if 'brand_instructions' in result:
                    print("Used Instructions:", result['brand_instructions'])
            else:
                print("No analysis found in response")
                print("Full response:", result)
                
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            print("Raw response:", response.text)
            return None

def process_followup_prompt(api_url: str, previous_analysis: str, followup_prompt: str):
    """
    Send a followup prompt based on previous analysis
    
    Args:
        api_url: The base URL of the API (e.g., 'http://localhost:8000')
        previous_analysis: The analysis from the first call
        followup_prompt: The prompt for further analysis
    """
    # Prepare the endpoint URL
    endpoint = f"{api_url}/process-prompt"
    
    # Prepare the form data
    data = {
        'previous_analysis': previous_analysis,
        'followup_prompt': followup_prompt
    }
    
    try:
        # Make the POST request
        response = requests.post(endpoint, data=data)
        response.raise_for_status()
        
        # Print the raw response for debugging
        print("\nFollowup Analysis Raw Response:", response.text)
        
        # Parse the JSON response
        result = response.json()
        
        # Check if there's an error in the response
        if 'error' in result:
            print("Error from server:", result['error'])
            return result
            
        # Print the analysis if available
        if 'analysis' in result:
            print("\nFollowup Analysis Result:", result['analysis'])
        else:
            print("No analysis found in response")
            print("Full response:", result)
            
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", response.text)
        return None

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