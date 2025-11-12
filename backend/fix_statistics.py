import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

from variants.models import Variant
from django.db.models import Count

print("=" * 60)
print("CHECKING CURRENT STATISTICS")
print("=" * 60)

total = Variant.objects.count()
print(f"\nTotal Variants: {total}")

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

if high == 1 and total > 100:
    print("\n" + "=" * 60)
    print("WARNING: Only 1 HIGH impact variant found!")
    print("This is likely due to fixed random seed.")
    print("\nTo fix: Reseed the database with:")
    print("  python manage.py seed_mock_data --variants 5000 --flush")
    print("=" * 60)

