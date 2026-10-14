def solve(root, names):
    """Повертає «ім'я: ok» або «ім'я: КОД_errno» для кожного імені."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print("\n".join(solve(sys.argv[1] if len(sys.argv) > 1 else ".", ["nofile"])))
