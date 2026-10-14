def solve(root):
    """Повертає текстовий звіт про дерево: кількості за типами, сумарний розмір, найбільший файл."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print(solve(sys.argv[1] if len(sys.argv) > 1 else "."))
