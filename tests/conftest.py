"""Допоміжний завантажувач і будівник дерев: підключає файл задачі з теки variants/."""
import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VARIANT_DIR = Path(os.environ.get("VARIANT_DIR", ROOT.parent / "variants"))
MTIME = 1_700_000_000


def load(number):
    """Повертає модуль задачі з номером number (1..10)."""
    path = VARIANT_DIR / f"variant_{number:02d}.py"
    if not path.exists():
        raise FileNotFoundError(f"Не знайдено файл задачі {number:02d} у {VARIANT_DIR}")
    spec = importlib.util.spec_from_file_location(f"variant_{number:02d}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_tree(root, entries):
    """Створює дерево за описом: ("d", шлях), ("f", шлях, розмір|байти, {mode, mtime}), ("l", шлях, ціль), ("h", шлях, існуючий)."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        kind, rel = entry[0], entry[1]
        full = root / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        if kind == "d":
            full.mkdir(parents=True, exist_ok=True)
        elif kind == "f":
            content = entry[2]
            opts = entry[3] if len(entry) > 3 else {}
            full.write_bytes(b"x" * content if isinstance(content, int) else content)
            mtime = opts.get("mtime", MTIME)
            os.utime(full, (mtime, mtime))
            os.chmod(full, opts.get("mode", 0o644))
        elif kind == "l":
            os.symlink(entry[2], full)
        elif kind == "h":
            os.link(root / entry[2], full)
        else:
            raise ValueError(f"невідомий тип запису {kind!r}")


def fill(value, root):
    """Підставляє каталог дерева замість префікса @root у аргументах."""
    if isinstance(value, str) and value.startswith("@root"):
        return str(root) + value[5:]
    if isinstance(value, list):
        return [fill(v, root) for v in value]
    if isinstance(value, tuple):
        return tuple(fill(v, root) for v in value)
    return value


def open_fds():
    """Список відкритих дескрипторів поточного процесу (Linux, /proc/self/fd)."""
    return sorted(int(name) for name in os.listdir("/proc/self/fd"))
