from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from variants.models import Variant

@api_view(['GET'])
def debug_statistics(request):
    queryset = Variant.objects.all()
    
    total = queryset.count()
    
    impact_breakdown = {}
    for impact in ['HIGH', 'MODERATE', 'LOW', 'MODIFIER']:
        count = queryset.filter(impact=impact).count()
        impact_breakdown[impact] = count
    
    null_impact = queryset.filter(impact__isnull=True).count()
    
    unique_genes = queryset.exclude(gene_symbol__isnull=True).values('gene_symbol').distinct().count()
    
    top_genes_raw = queryset.exclude(gene_symbol__isnull=True).values('gene_symbol').annotate(count=Count('id')).order_by('-count')[:10]
    top_genes = [{'name': g['gene_symbol'], 'count': g['count']} for g in top_genes_raw]
    
    return Response({
        'total_variants': total,
        'impact_breakdown': impact_breakdown,
        'null_impact_count': null_impact,
        'unique_genes_count': unique_genes,
        'top_genes': top_genes,
        'debug_info': {
            'impact_query_test': list(queryset.exclude(impact__isnull=True).values('impact').annotate(count=Count('id'))),
            'gene_query_test': list(queryset.exclude(gene_symbol__isnull=True).values('gene_symbol').distinct()[:5])
        }
    })

