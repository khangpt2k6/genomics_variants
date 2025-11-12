import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variants_project.settings')
django.setup()

from variants.models import Variant
from django.db.models import Count, Q

print("=" * 60)
print("DATABASE STATISTICS DEBUG")
print("=" * 60)

total = Variant.objects.count()
print(f"\nTotal Variants: {total}")

print("\nImpact Distribution:")
impact_counts = Variant.objects.exclude(impact__isnull=True).values('impact').annotate(count=Count('id')).order_by('impact')
for item in impact_counts:
    print(f"  {item['impact']}: {item['count']}")

null_impact = Variant.objects.filter(impact__isnull=True).count()
print(f"  NULL: {null_impact}")

print("\nUnique Genes:")
unique_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').distinct().count()
print(f"  Total Unique Genes: {unique_genes}")

print("\nTop 10 Genes:")
top_genes = Variant.objects.exclude(gene_symbol__isnull=True).values('gene_symbol').annotate(count=Count('id')).order_by('-count')[:10]
for gene in top_genes:
    print(f"  {gene['gene_symbol']}: {gene['count']}")

print("\nPathogenic Variants:")
pathogenic = Variant.objects.filter(clinical_significance__significance__in=['pathogenic', 'likely_pathogenic']).distinct().count()
print(f"  Count: {pathogenic}")

print("\n" + "=" * 60)
print("Raw Query Test:")
print("=" * 60)

high_count = Variant.objects.filter(impact='HIGH').count()
moderate_count = Variant.objects.filter(impact='MODERATE').count()
low_count = Variant.objects.filter(impact='LOW').count()
modifier_count = Variant.objects.filter(impact='MODIFIER').count()

print(f"HIGH: {high_count}")
print(f"MODERATE: {moderate_count}")
print(f"LOW: {low_count}")
print(f"MODIFIER: {modifier_count}")

