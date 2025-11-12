import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

from dotenv import load_dotenv
load_dotenv()

def test_gemini_import():
    print("=" * 60)
    print("TEST 1: Checking google-generativeai package...")
    print("=" * 60)
    try:
        import google.generativeai as genai
        print("[OK] google-generativeai package is installed")
        return True
    except ImportError as e:
        print(f"[ERROR] google-generativeai package not found: {e}")
        print("   Install with: pip install google-generativeai>=0.3.0")
        return False

def test_api_key():
    print("\n" + "=" * 60)
    print("TEST 2: Checking GEMINI_API_KEY...")
    print("=" * 60)
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and api_key != 'your_gemini_api_key_here':
        print(f"[OK] GEMINI_API_KEY is set (length: {len(api_key)} characters)")
        return True
    else:
        print("[ERROR] GEMINI_API_KEY is not set or is placeholder")
        print("   Set it in your .env file: GEMINI_API_KEY=your_key_here")
        return False

def test_gemini_service_init():
    print("\n" + "=" * 60)
    print("TEST 3: Testing GeminiService initialization...")
    print("=" * 60)
    try:
        from variants_project.gemini_service import GeminiService
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("[SKIP] Skipping - API key not configured")
            return None
        
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        service = GeminiService(model_name=model_name)
        print(f"[OK] GeminiService initialized successfully")
        print(f"   Model: {service.model_name}")
        return service
    except ValueError as e:
        print(f"[ERROR] Failed to initialize GeminiService: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return None

def test_simple_generation(service):
    print("\n" + "=" * 60)
    print("TEST 4: Testing simple text generation...")
    print("=" * 60)
    if not service:
        print("[SKIP] Skipping - Service not initialized")
        return False
    
    try:
        prompt = "Say 'Hello, Gemini integration is working!' in one sentence."
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        response = service.generate_text(prompt, temperature=0.7, max_tokens=100)
        print(f"[OK] Response received:")
        print(f"   {response[:200]}...")
        return True
    except Exception as e:
        print(f"[ERROR] Error generating text: {e}")
        if "429" in str(e) or "quota" in str(e).lower():
            print("   This might be a rate limit issue. Wait a minute and try again.")
        elif "API key" in str(e).lower():
            print("   Check your API key is valid at https://aistudio.google.com/app/apikey")
        return False

def test_variant_interpreter():
    print("\n" + "=" * 60)
    print("TEST 5: Testing VariantInterpreter (requires variant data)...")
    print("=" * 60)
    try:
        from variants.models import Variant
        from variants_project.gemini_service import VariantInterpreter
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("[SKIP] Skipping - API key not configured")
            return False
        
        variant = Variant.objects.first()
        if not variant:
            print("[SKIP] No variants found in database")
            print("   Seed data with: python manage.py seed_mock_data --variants 10")
            return None
        
        print(f"Testing with variant: {variant.variant_id}")
        interpreter = VariantInterpreter()
        
        print("Generating variant summary (this may take 10-30 seconds)...")
        result = interpreter.generate_variant_summary(variant)
        
        if 'error' in result:
            print(f"[ERROR] Error: {result.get('error')}")
            return False
        
        print("[OK] Variant summary generated successfully!")
        if 'interpretation' in result:
            interpretation = result['interpretation']
            if 'summary' in interpretation:
                print(f"   Summary preview: {interpretation['summary'][:150]}...")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def test_model_availability():
    print("\n" + "=" * 60)
    print("TEST 6: Testing model availability...")
    print("=" * 60)
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("[SKIP] Skipping - API key not configured")
            return False
        
        genai.configure(api_key=api_key)
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        
        print(f"Checking model: {model_name}")
        try:
            model = genai.GenerativeModel(model_name)
            print(f"[OK] Model '{model_name}' is available")
            return True
        except Exception as e:
            print(f"[ERROR] Model '{model_name}' not available: {e}")
            print("   Try: gemini-2.0-flash or gemini-pro")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error checking models: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("GEMINI API INTEGRATION TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    results['import'] = test_gemini_import()
    if not results['import']:
        print("\n[CRITICAL] Cannot proceed without google-generativeai package")
        print("   Install with: pip install google-generativeai>=0.3.0")
        return
    
    results['api_key'] = test_api_key()
    
    service = test_gemini_service_init()
    results['service_init'] = service is not None
    
    if service:
        results['generation'] = test_simple_generation(service)
    
    results['model'] = test_model_availability()
    
    results['variant_interpreter'] = test_variant_interpreter()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    total = sum(1 for v in results.values() if v is not None)
    
    for test_name, result in results.items():
        if result is True:
            print(f"[OK] {test_name}")
        elif result is False:
            print(f"[FAIL] {test_name}")
        else:
            print(f"[SKIP] {test_name}")
    
    print(f"\nPassed: {passed}/{total} tests")
    
    if passed == total and total > 0:
        print("\n[SUCCESS] All tests passed! Gemini integration is working correctly.")
    elif passed > 0:
        print("\n[WARNING] Some tests passed. Check failed tests above.")
    else:
        print("\n[FAILED] Tests failed. Please check the errors above.")

if __name__ == '__main__':
    main()
