"""显式新输出入口；竞赛原实现保存在 archive/competition-code。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from multibeam.__main__ import main


if __name__ == "__main__":
    main(["q3", *sys.argv[1:]])
