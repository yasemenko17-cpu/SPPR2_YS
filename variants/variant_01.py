def solve(root, ext, min_size, newer_than):
    """Повертає відсортований список шляхів звичайних файлів за розширенням, розміром і часом зміни."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print(solve(sys.argv[1] if len(sys.argv) > 1 else ".", ".py", 0, None))
