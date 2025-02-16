import requests

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

if __name__ == "__main__":
    # Example usage
    API_URL = "http://localhost:8000"
    FILE_PATH = "/home/navid/Pictures/Screenshots/IG_profile_example.png"
    INSTRUCTIONS = "Analyze a selection of an individual's Instagram photos to extract insights about their personality, lifestyle, aesthetic, and brand affinity. Use these insights to suggest the best tone, visual style, and storytelling approach for a hyper-personalized AI-generated ad that seamlessly aligns with their content and resonates with their audience."
    
    print("\nAnalyzing Local Image...")
    initial_result = process_local_file(API_URL, FILE_PATH, INSTRUCTIONS)
    
    if initial_result and 'analysis' in initial_result:
        # Example followup prompt
        # FOLLOWUP_PROMPT = "Based on the previous analysis, create a detailed storyboard for a 30-second video advertisement. Include specific visual scenes, transitions, and messaging that would resonate with this person's aesthetic and audience."
        FOLLOWUP_PROMPT = "Using the provided characteristics, create a detailed 20-second storyboard for a high-energy Coca-Cola advertisement tailored to this individual. The storyboard should be optimized for AI video generation software (e.g., Sora, Runway, Minimax, Luma) and include the following details:\nScene Breakdown – Provide a structured sequence of shots, ensuring smooth transitions and a compelling narrative arc.\nCamera Movements – Specify shot types to enhance the cinematic feel.\nLighting & Mood – Define the lighting conditions and overall atmosphere.\nEnvironmental Details – Include background elements that interact with the subject.\nsubject descrption: Describe the subject's appearence in each scene. Always describe the subject in each scene\nSubject Actions & Expressions – Clearly describe movements, facial expressions, and interactions with Coca-Cola to evoke refreshment, excitement, and freedom.\nEditing & Transitions – Indicate pacing to create dynamic storytelling.\nAudio & Sound Design – Include ambient sounds, music choices, and key sound effects .\nColor Palette & Visual Style – Describe the aesthetic using Coca-Cola's signature reds, deep ocean blues, and golden tones for an aspirational, lifestyle-focused look.\nText & Branding Elements – Ensure Coca-Cola branding, tagline placement, and product visibility are naturally integrated within the visuals. Instead of using the persons name, describe him briefly DO not use emojis\nDescribe the actions as easy as possible and as clear as possible\nEach scene should start with the description what the subject looks like physically"
        
        print("\nProcessing followup analysis...")
        followup_result = process_followup_prompt(API_URL, initial_result['analysis'], FOLLOWUP_PROMPT) 