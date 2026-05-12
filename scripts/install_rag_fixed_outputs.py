"""Install fixed RAG artifacts from Colab into the main project.

Expected zip file from Colab:
rag_data_upgrade_experiment_fixed_outputs.zip

The script backs up current Module 4 data/index files before replacing them.
"""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


EXPECTED = {
    "corpus": "rag_corpus_expanded_module4_fixed.csv",
    "index": "models_module4_expanded_fixed/review_faiss_expanded_fixed.index",
    "metadata": "models_module4_expanded_fixed/review_metadata_expanded_fixed.parquet",
    "config": "models_module4_expanded_fixed/module4_index_config_expanded_fixed.json",
}


DESTINATIONS = {
    "corpus": Path("data/processed/rag_corpus_module4.csv"),
    "index": Path("models/module4/review_faiss.index"),
    "metadata": Path("models/module4/review_metadata.parquet"),
    "config": Path("models/module4/module4_index_config.json"),
}


def find_default_zip() -> Path | None:
    candidates = [
        Path.home() / "Downloads" / "rag_data_upgrade_experiment_fixed_outputs.zip",
        PROJECT_DIR.parent / "rag_data_upgrade_experiment_fixed_outputs.zip",
        PROJECT_DIR / "rag_data_upgrade_experiment_fixed_outputs.zip",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def validate_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    missing = [path for path in EXPECTED.values() if path not in names]
    if missing:
        raise FileNotFoundError(
            "Zip does not contain expected fixed RAG files:\n" + "\n".join(missing)
        )


def backup_existing(project_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = project_dir / "backups" / f"rag_module4_before_upgrade_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for key, relative_path in DESTINATIONS.items():
        source = project_dir / relative_path
        if source.exists():
            target = backup_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return backup_dir


def install(zip_path: Path, project_dir: Path) -> None:
    validate_zip(zip_path)
    backup_dir = backup_existing(project_dir)

    temp_dir = project_dir / "backups" / "_tmp_rag_fixed_extract"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(temp_dir)

        for key, expected_path in EXPECTED.items():
            source = temp_dir / expected_path
            target = project_dir / DESTINATIONS[key]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        config_path = project_dir / DESTINATIONS["config"]
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["index_path"] = "models/module4/review_faiss.index"
        config["metadata_path"] = "models/module4/review_metadata.parquet"
        config["input_path"] = "data/processed/rag_corpus_module4.csv"
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    print("Installed fixed RAG artifacts.")
    print(f"Project: {project_dir}")
    print(f"Backup: {backup_dir}")
    for key, relative_path in DESTINATIONS.items():
        path = project_dir / relative_path
        print(f"{key}: {path} ({path.stat().st_size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install fixed RAG artifacts into project.")
    parser.add_argument("--zip", default=None, help="Path to rag_data_upgrade_experiment_fixed_outputs.zip")
    parser.add_argument("--project_dir", default=str(PROJECT_DIR))
    args = parser.parse_args()

    zip_path = Path(args.zip).expanduser().resolve() if args.zip else find_default_zip()
    if zip_path is None or not zip_path.exists():
        raise FileNotFoundError(
            "Could not find rag_data_upgrade_experiment_fixed_outputs.zip. "
            "Pass it explicitly with --zip."
        )
    install(zip_path, Path(args.project_dir).expanduser().resolve())


if __name__ == "__main__":
    main()
