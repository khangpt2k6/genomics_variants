import requests
import json

url = "http://localhost:8000/api/variants/statistics/"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("=" * 60)
    print("API STATISTICS RESPONSE")
    print("=" * 60)
    print(json.dumps(data, indent=2))
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Variants: {data.get('total_variants', 0)}")
    print(f"Pathogenic: {data.get('pathogenic_variants', 0)}")
    print(f"\nImpact Counts:")
    for impact, count in data.get('impact_counts', {}).items():
        print(f"  {impact}: {count}")
    print(f"\nUnique Genes: {data.get('unique_genes_count', 0)}")
    print(f"\nTop Genes:")
    for gene in data.get('top_genes', [])[:5]:
        print(f"  {gene.get('name')}: {gene.get('count')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

