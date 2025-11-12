import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

from variants.models import Variant
from django.db.models import Count

print("=" * 60)
print("AUTOMATED DASHBOARD STATISTICS TEST")
print("=" * 60)

total = Variant.objects.count()
print(f"\nTotal Variants: {total}")

if total == 0:
    print("\n[WARNING] No variants found in database!")
    print("Run: python manage.py seed_mock_data --variants 5000 --flush")
    sys.exit(1)

print("\nImpact Distribution:")
high = Variant.objects.filter(impact='HIGH').count()
moderate = Variant.objects.filter(impact='MODERATE').count()
low = Variant.objects.filter(impact='LOW').count()
modifier = Variant.objects.filter(impact='MODIFIER').count()
null_impact = Variant.objects.filter(impact__isnull=True).count()

print(f"  HIGH: {high}")
print(f"  MODERATE: {moderate}")
print(f"  LOW: {low}")
print(f"  MODIFIER: {modifier}")
print(f"  NULL: {null_impact}")

unique_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').distinct().count()
print(f"\nUnique Genes: {unique_genes}")

print("\nTop 5 Genes:")
top_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').annotate(count=Count('id')).order_by('-count')[:5]
for gene in top_genes:
    print(f"  {gene['gene_symbol']}: {gene['count']}")

print("\n" + "=" * 60)
print("TEST RESULTS")
print("=" * 60)

issues = []

if high == 1 and total > 100:
    issues.append("Only 1 HIGH impact variant found (expected more with random distribution)")

if unique_genes == 0:
    issues.append("No unique genes found")

if total < 100:
    issues.append(f"Low variant count ({total}), consider seeding more data")

if issues:
    print("\n[ISSUES FOUND]:")
    for issue in issues:
        print(f"  - {issue}")
    print("\n[RECOMMENDATION]:")
    print("  Run: python manage.py seed_mock_data --variants 5000 --flush")
else:
    print("\n[OK] Dashboard statistics look good!")
    print(f"  - Total variants: {total}")
    print(f"  - Impact distribution: HIGH={high}, MODERATE={moderate}, LOW={low}, MODIFIER={modifier}")
    print(f"  - Unique genes: {unique_genes}")

print("\n" + "=" * 60)

