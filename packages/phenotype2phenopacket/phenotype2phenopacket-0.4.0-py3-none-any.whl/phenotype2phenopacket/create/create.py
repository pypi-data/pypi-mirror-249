import random
from pathlib import Path

import polars as pl

from phenotype2phenopacket.utils.phenopacket_utils import (
    PhenotypeAnnotationToPhenopacketConverter,
    SyntheticPatientGenerator,
    write_phenopacket,
)
from phenotype2phenopacket.utils.utils import (
    get_phenotype_annotation_version,
    load_ontology,
    load_ontology_factory,
    read_phenotype_annotation_file,
)


def create_synthetic_patient_phenopacket(
    human_phenotype_ontology,
    omim_disease: pl.DataFrame,
    ontology_factory,
    output_dir: Path,
    hpoa_version: str,
):
    """Create a synthetic patient phenopacket from a set of phenotype entries for a specific OMIM disease."""
    synthetic_patient_generator = SyntheticPatientGenerator(
        omim_disease, human_phenotype_ontology, ontology_factory
    )
    patient_terms = synthetic_patient_generator.patient_term_annotation_set()
    phenopacket_file = PhenotypeAnnotationToPhenopacketConverter(
        human_phenotype_ontology
    ).create_phenopacket(patient_terms, hpoa_version, synthetic_patient_generator.get_onset_range())
    write_phenopacket(
        phenopacket_file.phenopacket, output_dir.joinpath(phenopacket_file.phenopacket_path)
    )


def create_synthetic_patients(phenotype_annotation: Path, num_disease: int, output_dir: Path):
    """Create a set of synthetic patient phenopackets from a phenotype annotation file."""
    phenotype_annotation_df = read_phenotype_annotation_file(phenotype_annotation)
    phenotype_annotation_version = get_phenotype_annotation_version(phenotype_annotation)
    human_phenotype_ontology = load_ontology()
    ontology_factory = load_ontology_factory()
    omim_diseases = phenotype_annotation_df.filter(
        pl.col("database_id").str.starts_with("OMIM")
    ).filter(pl.col("aspect") == "P")
    grouped_omim_diseases = omim_diseases.partition_by(by="database_id", maintain_order=True)
    if num_disease != 0:
        grouped_omim_diseases = random.sample(grouped_omim_diseases, num_disease)
    for omim_disease in grouped_omim_diseases:
        create_synthetic_patient_phenopacket(
            human_phenotype_ontology,
            omim_disease,
            ontology_factory,
            output_dir,
            phenotype_annotation_version,
        )
