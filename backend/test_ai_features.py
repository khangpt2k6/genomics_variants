import os
import sys
import django
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

BASE_URL = "http://localhost:8000"

def test_statistics_api():
    print("=" * 60)
    print("TESTING STATISTICS API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/variants/statistics/")
        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Statistics API working")
            print(f"Total Variants: {data.get('total_variants', 0)}")
            print(f"Pathogenic: {data.get('pathogenic_variants', 0)}")
            print(f"\nImpact Counts:")
            for impact, count in data.get('impact_counts', {}).items():
                print(f"  {impact}: {count}")
            print(f"\nUnique Genes: {data.get('unique_genes_count', 0)}")
            return True
        else:
            print(f"\n[ERROR] Statistics API failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"\n[ERROR] Statistics API error: {e}")
        return False

def test_trend_prediction():
    print("\n" + "=" * 60)
    print("TESTING TREND PREDICTION API")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/trend-prediction/",
            json={"days_ahead": 30},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Trend Prediction API working")
            print(f"Prediction ID: {data.get('prediction_id', 'N/A')}")
            print(f"Trend Direction: {data.get('predictions', {}).get('trend_direction', 'N/A')}")
            print(f"Confidence Score: {data.get('confidence_score', 0):.2%}")
            return True
        else:
            print(f"\n[ERROR] Trend Prediction API failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"\n[ERROR] Trend Prediction API error: {e}")
        return False

def test_graph_generation():
    print("\n" + "=" * 60)
    print("TESTING GRAPH GENERATION API")
    print("=" * 60)
    
    test_data = {
        "genes": ["BRCA1", "BRCA2", "TP53", "EGFR"],
        "counts": [150, 120, 100, 80]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/generate-graph/",
            json={"data": test_data, "graph_type": "bar"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Graph Generation API working")
            print(f"Generated graphs: {list(data.get('graphs', {}).keys())}")
            return True
        else:
            print(f"\n[ERROR] Graph Generation API failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"\n[ERROR] Graph Generation API error: {e}")
        return False

def test_variant_statistics_graph():
    print("\n" + "=" * 60)
    print("TESTING VARIANT STATISTICS GRAPH API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/ai/variant-statistics-graph/")
        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Variant Statistics Graph API working")
            print(f"Generated graphs: {list(data.get('graphs', {}).keys())}")
            return True
        else:
            print(f"\n[ERROR] Variant Statistics Graph API failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"\n[ERROR] Variant Statistics Graph API error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AI FEATURES TEST SUITE")
    print("=" * 60)
    print("\nMake sure Django server is running on http://localhost:8000")
    print("Press Enter to continue...")
    input()
    
    results = []
    
    results.append(("Statistics API", test_statistics_api()))
    results.append(("Trend Prediction", test_trend_prediction()))
    results.append(("Graph Generation", test_graph_generation()))
    results.append(("Variant Statistics Graph", test_variant_statistics_graph()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "[OK]" if result else "[FAILED]"
        print(f"{status} {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[WARNING] Some tests failed. Check errors above.")

