#!/usr/bin/env python3
"""Generate a pinned OpenAPI spec from the FastAPI app.

Usage:
  python scripts/generate_openapi.py --out openapi.json

This imports `api.main:app` directly (no server required) and writes the
OpenAPI JSON. Keeping this file in the repo enables client/type generation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OpenAPI JSON from FastAPI app")
    parser.add_argument(
        "--out",
        default="openapi.json",
        help="Output path for the OpenAPI JSON (default: openapi.json)",
    )
    args = parser.parse_args()

    # When executed as `python scripts/generate_openapi.py`, Python puts the
    # scripts folder on sys.path. Add the project root so `import api` works.
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Import here so the script is cheap to import/test.
    from api.main import app  # pylint: disable=import-outside-toplevel

    spec = app.openapi()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Deterministic output helps diffs and PR reviews.
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Wrote OpenAPI spec to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
