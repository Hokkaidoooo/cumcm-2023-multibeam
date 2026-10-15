"""记录或核验须保持原样的论文、历史工作簿和图片。"""
import argparse
from hashlib import sha256
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path = root / "docs" / "preserved-files.json"
    records = {p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest() for folder in ("code", "paper") for p in sorted((root / folder).rglob("*")) if p.is_file() and p.suffix.lower() in (".xlsx", ".png", ".jpg", ".pdf")}
    if args.verify:
        expected = json.loads(path.read_text(encoding="utf-8"))
        if records != expected:
            raise ValueError("historical file set or SHA-256 changed")
        print(f"Verified {len(records)} preserved files")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(records, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Recorded {len(records)} preserved files")


if __name__ == "__main__":
    main()
