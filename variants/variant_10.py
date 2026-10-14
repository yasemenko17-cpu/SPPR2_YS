def solve(path, data, mode):
    """Атомарно замінює вміст файла: тимчасовий файл, fsync, rename. Повертає кількість байтів."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    print(solve("conf.ini", b"hello\n", 0o644))
