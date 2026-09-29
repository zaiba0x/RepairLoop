import os
from hindsight_client import Hindsight

api_key = os.getenv("HINDSIGHT_API_KEY")

print("API key found:", bool(api_key))

if not api_key:
    print("API key is missing. Set it in the terminal.")
else:
    print("API key is available!")