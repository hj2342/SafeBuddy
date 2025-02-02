# # pip install python-dotenv
# #pip install requests
# # Install required packages first:
# # pip install python-dotenv requests
# # from together_AI import Together
# from together import Together
# from dotenv import load_dotenv
# import os

# load_dotenv()
# api_key = os.getenv("TOGETHER_API_KEY")

# client = Together(api_key=api_key)

# response = client.chat.completions.create(
#     model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
#     messages=[{"role": "user", "content": "I am at 40.512000, -74.250000 is this place safe. Recommend nearest safe areas and how to get there"}],
# )

# print(response.choices[0].message.content)
from together import Together
from dotenv import load_dotenv
import os

# Explicitly load .env file with debug
load_dotenv('.env')  # Specify path if not in same directory

# Debug: Verify environment variables
print("Current working directory:", os.getcwd())
print("Environment variables loaded:", 'TOGETHER_API_KEY' in os.environ)

# Initialize client with explicit key handling
try:
    api_key = os.getenv("TOGETHER_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Check .env file and path")
        
    client = Together(api_key=api_key)  # Explicitly pass API key
    
   # Create request with safety parameters
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{
            "role": "user", 
            "content": "I am at 40.512000, -74.250000 is this place safe. Recommend nearest safe areas and how to get there"
        }],
        max_tokens=500,
        temperature=0.7
    )
    
    # Print formatted response
    print("="*50)
    print("SAFETY RECOMMENDATIONS:")
    print(response.choices[0].message.content)
    print("="*50)
    print(f"Model: {response.model}")
    print(f"Tokens Used: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    if "404" in str(e):
        print("Possible solutions:")
        print("1. Check model name spelling")
        print("2. Verify model availability in your Together AI account")
    elif "401" in str(e):
        print("Authentication failed. Check:")
        print("1. .env file contains TOGETHER_API_KEY=your_actual_key")
        print("2. Key has correct permissions")    
except Exception as e:
    print(f"Error: {str(e)}")
