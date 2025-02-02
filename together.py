# pip install python-dotenv
#pip install requests
# Install required packages first:
# pip install python-dotenv requests
from SafeBuddy.together import Together
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=api_key)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "I am at 40.512000, -74.250000 is this place safe. Recommend nearest safe areas and how to get there"}],
)

print(response.choices[0].message.content)
