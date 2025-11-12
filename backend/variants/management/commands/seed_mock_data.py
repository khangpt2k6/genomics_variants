import random
from datetime import date, timedelta, datetime

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone

from faker import Faker

from variants.models import (
    Variant,
    ClinicalSignificance,
    DrugResponse,
    COSMICData,
    VariantAnnotation,
)


class Command(BaseCommand):
    help = "Seed the database with realistic mock variant data and related records."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--variants",
            type=int,
            default=50,
            help="Number of Variant records to create",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data for these models before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker()
        import time
        seed_value = int(time.time()) if options.get("variants", 50) > 100 else 42
        Faker.seed(seed_value)
        random.seed(seed_value)

        num_variants: int = options["variants"]
        do_flush: bool = options["flush"]

        if do_flush:
            self.stdout.write("Flushing existing data ...")
            VariantAnnotation.objects.all().delete()
            ClinicalSignificance.objects.all().delete()
            DrugResponse.objects.all().delete()
            COSMICData.objects.all().delete()
            Variant.objects.all().delete()

        self.stdout.write(self.style.WARNING(f"Seeding {num_variants} variants ..."))

        chromosomes = [str(c) for c in range(1, 23)] + ["X", "Y"]
        consequences = [
            "missense_variant",
            "synonymous_variant",
            "stop_gained",
            "frameshift_variant",
            "intron_variant",
            "splice_acceptor_variant",
            "splice_donor_variant",
        ]
        impacts = [choice for choice, _ in Variant.IMPACT_CHOICES]

        response_types = [choice for choice, _ in DrugResponse.RESPONSE_TYPE_CHOICES]
        evidence_levels = [choice for choice, _ in DrugResponse.EVIDENCE_LEVEL_CHOICES]
        evidence_directions = [choice for choice, _ in DrugResponse.EVIDENCE_DIRECTION_CHOICES]

        significance_choices = [choice for choice, _ in ClinicalSignificance.SIGNIFICANCE_CHOICES]
        review_status_choices = [choice for choice, _ in ClinicalSignificance.REVIEW_STATUS_CHOICES]

        created_variants = []

        for i in range(num_variants):
            chrom = random.choice(chromosomes)
            pos = random.randint(10_000, 250_000_000)
            ref = random.choice(["A", "C", "G", "T"]) * random.choice([1, 1, 1, 2])
            alt = random.choice([b for b in ["A", "C", "G", "T"] if b != ref[0]]) * random.choice([1, 1, 2])

            gene = random.choice([
                "BRCA1", "BRCA2", "TP53", "EGFR", "ALK", "KRAS", "NRAS", "BRAF", "PIK3CA",
                None, None  # allow missing gene_symbol
            ])
            transcript = None if not gene else f"{gene}-201"

            hgvs_c = None if not gene else f"c.{random.randint(1, 3000)}{random.choice(['A>G','C>T','del','dup'])}"
            hgvs_p = None if not gene else f"p.{random.choice(['Val','Ala','Gly','Ser'])}{random.randint(1, 1000)}{random.choice(['Met','Leu','*'])}"

            variant_id = f"{chrom}-{pos}-{ref}-{alt}-{i}"

            g_af = round(random.random() * random.random(), 6)  # skew to lower freqs
            g_afr = round(g_af * random.uniform(0.5, 1.2), 6)
            g_amr = round(g_af * random.uniform(0.5, 1.2), 6)
            g_eas = round(g_af * random.uniform(0.5, 1.2), 6)
            g_nfe = round(g_af * random.uniform(0.5, 1.2), 6)
            g_sas = round(g_af * random.uniform(0.5, 1.2), 6)

            variant = Variant(
                chromosome=chrom,
                position=pos,
                reference_allele=ref,
                alternate_allele=alt,
                variant_id=variant_id,
                quality_score=round(random.uniform(10, 1000), 2),
                filter_status=random.choice(["PASS", "q10", "s50", None]),
                gene_symbol=gene,
                transcript_id=transcript,
                hgvs_c=hgvs_c,
                hgvs_p=hgvs_p,
                consequence=random.choice(consequences),
                impact=random.choice(impacts) if random.random() > 0.1 else None,
                gnomad_af=g_af,
                gnomad_af_afr=min(g_afr, 1.0),
                gnomad_af_amr=min(g_amr, 1.0),
                gnomad_af_eas=min(g_eas, 1.0),
                gnomad_af_nfe=min(g_nfe, 1.0),
                gnomad_af_sas=min(g_sas, 1.0),
                vcf_data={
                    "DP": random.randint(10, 500),
                    "MQ": round(random.uniform(20, 60), 2),
                    "QD": round(random.uniform(1, 30), 2),
                },
            )

            # Validate to respect model clean() rules
            variant.full_clean(exclude=None)
            variant.save()
            
            # Set random created_at date for trend analysis (spread over last 6 months)
            days_ago = random.randint(0, 180)
            random_date = timezone.now() - timedelta(days=days_ago)
            Variant.objects.filter(pk=variant.pk).update(created_at=random_date)
            variant.refresh_from_db()
            
            created_variants.append(variant)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_variants)} Variant records."))

        # Related records per variant
        total_cs = total_dr = total_cosmic = total_ann = 0
        for v in created_variants:
            # ClinicalSignificance: 0-2 per variant
            for _ in range(random.choice([0, 1, 1, 2])):
                cs = ClinicalSignificance(
                    variant=v,
                    significance=random.choice(significance_choices),
                    review_status=random.choice(review_status_choices + [None, None]),
                    review_date=date.today() - timedelta(days=random.randint(0, 3650)),
                    clinvar_id=str(random.randint(100000, 999999)) if random.choice([True, False]) else None,
                    evidence_level=random.choice(["1", "2A", "2B", None]),
                    phenotype=random.choice([
                        "Breast cancer",
                        "Lung adenocarcinoma",
                        "Melanoma",
                        None,
                    ]),
                    inheritance_pattern=random.choice(["Autosomal dominant", "Autosomal recessive", None]),
                    clinvar_data={"submitters": random.randint(1, 5)},
                )
                try:
                    cs.full_clean()
                    cs.save()
                    total_cs += 1
                except Exception:
                    # Skip duplicates on (variant, clinvar_id)
                    pass

            # DrugResponse: 0-3 per variant
            for _ in range(random.choice([0, 1, 2, 3])):
                dr = DrugResponse(
                    variant=v,
                    drug_name=random.choice([
                        "Trastuzumab",
                        "Gefitinib",
                        "Vemurafenib",
                        "Imatinib",
                        "Cetuximab",
                    ]),
                    response_type=random.choice(response_types),
                    evidence_level=random.choice(evidence_levels),
                    evidence_direction=random.choice(evidence_directions),
                    civic_id=str(random.randint(1000, 9999)) if random.choice([True, False]) else None,
                    evidence_id=str(random.randint(10000, 99999)) if random.choice([True, False]) else None,
                    cancer_type=random.choice([
                        "Breast carcinoma",
                        "Colorectal carcinoma",
                        "Non-small cell lung carcinoma",
                        None,
                    ]),
                    tissue_type=random.choice(["Tumor", "Normal", None]),
                    civic_data={"evidence_items": random.randint(1, 10)},
                )
                try:
                    dr.full_clean()
                    dr.save()
                    total_dr += 1
                except Exception:
                    # Skip duplicates on (variant, civic_id)
                    pass

            # COSMICData: 0-1 per variant
            if random.choice([True, False]):
                cosmic = COSMICData(
                    variant=v,
                    cosmic_id=f"COSM{random.randint(100000, 999999)}",
                    mutation_description=random.choice([
                        "Substitution - Missense",
                        "Deletion",
                        "Insertion",
                        None,
                    ]),
                    mutation_cds=random.choice(["c.123A>G", "c.456del", None]),
                    mutation_aa=random.choice(["p.Val41Ala", "p.Gly12Asp", None]),
                    primary_site=random.choice(["breast", "lung", "skin", None]),
                    site_subtype=random.choice(["ductal", "adenocarcinoma", None]),
                    primary_histology=random.choice(["carcinoma", "melanoma", None]),
                    histology_subtype=random.choice(["ductal carcinoma", "squamous", None]),
                    sample_name=fake.bothify(text="SAMPLE-####"),
                    sample_source=random.choice(["biopsy", "surgical", None]),
                    tumour_origin=random.choice([choice for choice, _ in COSMICData.TUMOUR_ORIGIN_CHOICES] + [None]),
                    mutation_frequency=round(random.random() * random.random(), 6),
                    mutation_count=random.randint(1, 500),
                    cosmic_data={"accession": fake.uuid4()},
                )
                try:
                    cosmic.full_clean()
                    cosmic.save()
                    total_cosmic += 1
                except Exception:
                    # Unique cosmic_id collisions are unlikely but safe-guard
                    pass

            # VariantAnnotation (1 per variant)
            has_dr = v.drug_responses.exists()
            has_cs = v.clinical_significance.exists()
            has_cos = v.cosmic_data.exists()

            annot = VariantAnnotation(
                variant=v,
                is_pathogenic=has_cs and any(cs.is_pathogenic() for cs in v.clinical_significance.all()),
                is_drug_target=has_dr,
                has_cosmic_data=has_cos,
                pathogenicity_score=(round(random.uniform(0.2, 0.98), 3) if has_cs else None),
                drug_response_score=(round(random.uniform(0.2, 0.98), 3) if has_dr else None),
                annotation_version="1.0",
                annotation_data={
                    "summary": [s for s in [
                        "Pathogenic" if has_cs else None,
                        "Drug Target" if has_dr else None,
                        "COSMIC Data" if has_cos else None,
                    ] if s],
                },
            )
            annot.full_clean()
            annot.save()
            total_ann += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created: {total_cs} ClinicalSignificance, {total_dr} DrugResponse, {total_cosmic} COSMICData, {total_ann} VariantAnnotation"
        ))

        self.stdout.write(self.style.SUCCESS("Seeding complete."))


