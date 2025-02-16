import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file located in the same directory
load_dotenv()



# import requests
#
# # API endpoint URL
# url = "http://localhost:8000/process-screenshot"
#
# try:
#     # Example with brand instructions
#     data = {
#         'brand_instructions': 'Make it look modern and professional'
#     }
#
#     # Make request without image but with instructions
#     response = requests.post(url, data=data)
#
#     # Print the response
#     print("API Response:", response.json())
#
# except requests.exceptions.ConnectionError:
#     print("Error: Could not connect to the API. Make sure the server is running.")
# except requests.exceptions.RequestException as e:
#     print(f"Error making request: {e}")