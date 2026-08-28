# clustering_docx.py
"""Script per fer clústers en base a les metadades
d'un conjunt d'arxius de Word (extensió .docx)."""

import hashlib
import zipfile

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


# Config _______________________________________________________________________

ROOT_FOLDER = Path(
    r"C:\Users\55182183p\OneDrive - Generalitat de Catalunya\Obsidian_vaults\Gencat Energia\Bloc C - Plantilles\Plantilles\Plantilles originals per tràmits"
)
"""Farem clústers amb els documents continguts aquí
    (poden estar en subcarpetes)."""

# Data structures, helpers and format __________________________________________

@dataclass
class DocMetadata:
    path: Path
    metadata_files: dict
    fingerprint: str


def sha256_text(text) -> str:
    """Hash."""
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def build_clusters(documents) -> dict:

    clusters = defaultdict(list)

    for doc in documents:
        clusters[doc.fingerprint].append(doc)

    return clusters


def print_metadata(metadata):

    for name, content in metadata.items():
        print()
        print("\n" + f"[{name}]")

        if content is None:
            print("<NO EXISTEIX>")
        else:
            print(content)


# Extraction ___________________________________________________________________

def extract_metadata(docx_path):

    metadata_files = {}

    with zipfile.ZipFile(docx_path) as z:

        for name in [
            "docProps/core.xml",
            "docProps/app.xml",
            "docProps/custom.xml"
        ]:

            if name in z.namelist():
                metadata_files[name] = z.read(name).decode("utf-8", errors="ignore")

            else:
                metadata_files[name] = None

    fingerprint_source = ""

    for key in sorted(metadata_files):

        fingerprint_source += (f"\n### {key} ###\n")

        fingerprint_source += (metadata_files[key] if metadata_files[key] else "<MISSING>")

    fingerprint = sha256_text(fingerprint_source)

    return DocMetadata(
        path=docx_path,
        metadata_files=metadata_files,
        fingerprint=fingerprint
    )


# Main _________________________________________________________________________

def main():

    docs = []

    print("Llegint documents...")

    for file in ROOT_FOLDER.rglob("*.docx"):
        try:
            docs.append(extract_metadata(file))

        except Exception as ex:
            print("\n" + "ERROR:", file)
            print(ex)

    print("\n" + "=" * 80)
    print("CLUSTERING PER METADADES")
    print("=" * 80 + "\n")

    clusters = build_clusters(docs)

    print(f"Documents analitzats: {len(docs)}")
    print(f"Clusters detectats: {len(clusters)}")

    sorted_clusters = sorted(
        clusters.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    for cluster_index, (fingerprint, cluster_docs) in enumerate(sorted_clusters, start=1):

        print("\n" + "=" * 80)
        print(f"CLUSTER {cluster_index}")
        print("=" * 80 + "\n")

        print(f"Fingerprint: {fingerprint}")
        print(f"Documents: {len(cluster_docs)}")

        print("\nDOCUMENTS\n---------")

        for doc in cluster_docs:
            print(doc.path)

        print("\nMETADADES\n---------")

        print_metadata(cluster_docs[0].metadata_files)

    print("\n" + "=" * 80)
    print("RESUM")
    print("=" * 80)

    for cluster_index, (fingerprint, cluster_docs) in enumerate(sorted_clusters, start=1):

        print(f"Cluster {cluster_index:3d} | " f"{len(cluster_docs):5d} documents")

main()