import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

from variants.models import Variant
from django.db.models import Count

print("=" * 60)
print("CHECKING VARIANT DISTRIBUTION")
print("=" * 60)

total = Variant.objects.count()
print(f"\nTotal Variants: {total}")

print("\nImpact Distribution:")
impact_counts = Variant.objects.values('impact').annotate(count=Count('id')).order_by('-count')
for item in impact_counts:
    impact = item['impact'] or 'NULL'
    count = item['count']
    percentage = (count / total * 100) if total > 0 else 0
    print(f"  {impact}: {count} ({percentage:.1f}%)")

print("\nUnique Genes:")
unique_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').distinct().count()
print(f"  Count: {unique_genes}")

print("\nTop 10 Genes by Count:")
top_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').annotate(count=Count('id')).order_by('-count')[:10]
for gene in top_genes:
    print(f"  {gene['gene_symbol']}: {gene['count']}")

print("\n" + "=" * 60)
print("ANALYSIS")
print("=" * 60)

high_count = Variant.objects.filter(impact='HIGH').count()
if high_count == 1 and total > 100:
    print("\n[ISSUE] Only 1 HIGH impact variant found!")
    print("Expected: ~1125 HIGH impact variants (25% of 90% with impact)")
    print("This suggests the seed script needs better distribution.")

if unique_genes == 9:
    print("\n[OK] 9 unique genes matches seed script (9 genes defined)")
else:
    print(f"\n[INFO] Found {unique_genes} unique genes")

