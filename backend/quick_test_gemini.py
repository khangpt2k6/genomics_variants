import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

print("Loading .env from:", env_path)
print("File exists:", env_path.exists())

load_dotenv(dotenv_path=env_path)

api_key = os.getenv('GEMINI_API_KEY')
model = os.getenv('GEMINI_MODEL')

print("\nEnvironment Variables:")
print(f"GEMINI_API_KEY: {'SET' if api_key else 'NOT SET'}")
if api_key:
    print(f"  Value: {api_key[:20]}...")
print(f"GEMINI_MODEL: {model}")

if api_key:
    print("\n[OK] GEMINI_API_KEY is loaded correctly!")
    print("\nNext step: Restart your Django server to apply the fix.")
else:
    print("\n[ERROR] GEMINI_API_KEY is not loaded!")
    print("Check that .env file is in:", BASE_DIR)

