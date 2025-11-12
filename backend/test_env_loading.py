import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')

print("=" * 60)
print("TESTING ENVIRONMENT VARIABLE LOADING")
print("=" * 60)

print(f"\nBASE_DIR: {BASE_DIR}")
print(f".env file path: {BASE_DIR / '.env'}")
print(f".env file exists: {(BASE_DIR / '.env').exists()}")

from dotenv import load_dotenv
load_dotenv(dotenv_path=BASE_DIR / '.env')

print("\nEnvironment Variables:")
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"GEMINI_API_KEY: {gemini_key[:20]}... (hidden)")
else:
    print("GEMINI_API_KEY: NOT SET")

gemini_model = os.getenv('GEMINI_MODEL')
print(f"GEMINI_MODEL: {gemini_model}")

print("\n" + "=" * 60)
print("Testing Django settings load...")
print("=" * 60)

try:
    django.setup()
    print("[OK] Django settings loaded successfully")
    
    from variants_project.gemini_ai_services import get_trend_predictor
    print("\nTesting Gemini service initialization...")
    predictor = get_trend_predictor()
    print("[OK] Gemini service initialized successfully!")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

