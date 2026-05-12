"""Run the FastAPI + frontend RAG demo."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RAG web demo.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parents[1]
    os.chdir(project_dir)
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))

    try:
        import uvicorn
    except ImportError as exc:
        raise SystemExit(
            "Missing web dependencies. Run: python -m pip install -r requirements_webapp.txt"
        ) from exc

    uvicorn.run(
        "backend.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
