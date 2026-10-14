"""Створює дерево свого варіанта для ручного запуску.

Використання:  python build_dataset.py <номер варіанта 1..30> <каталог>
Каталог буде створено; вихідні дані варіанта розміщуються в підкаталозі data.
Скрипт друкує номер задачі й виклик solve(...), який відтворює картку.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from conftest import fill, make_tree  # noqa: E402
from test_variants import DATA  # noqa: E402


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    number = int(sys.argv[1])
    if not 1 <= number <= 30:
        print("Номер варіанта має бути від 1 до 30")
        return 1
    task = (number - 1) // 3 + 1
    case = DATA[task]["sets"][(number - 1) % 3]
    root = Path(sys.argv[2]).resolve() / "data"
    make_tree(root, case["tree"])
    print(f"Задача {task}, файл variants/variant_{task:02d}.py")
    print(f"Каталог з даними: {root}")
    print("Виклик: solve(" + ", ".join(repr(a) for a in fill(case["args"], root)) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
