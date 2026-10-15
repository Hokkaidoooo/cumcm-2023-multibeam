import argparse
import json
from pathlib import Path

from .experiments import environment, question1, question2, question3, question4_audit


def main(argv=None):
    parser = argparse.ArgumentParser(description="水平几何计算、历史差异和测线约束验证")
    parser.add_argument("experiment", choices=("q1", "q2", "q3", "q4-audit", "all"))
    parser.add_argument("--output", type=Path, required=True, help="必须是尚不存在的新输出目录")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    operations = {"q1": question1, "q2": lambda: question2(root), "q3": question3, "q4-audit": lambda: question4_audit(root)}
    selected = operations if args.experiment == "all" else {args.experiment: operations[args.experiment]}
    results = {name: operation() for name, operation in selected.items()}
    args.output.mkdir(parents=True, exist_ok=False)
    for name, value in results.items():
        (args.output / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (args.output / "environment.json").write_text(json.dumps(environment(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(results)} experiment reports to {args.output}")
    if "q4-audit" in results:
        print("Q4 reconstruction incomplete: original attachment and dataset-2 generation rules are missing.")


if __name__ == "__main__":
    main()
