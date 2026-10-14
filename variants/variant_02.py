def solve(root, required):
    """Повертає рядки «шлях права-рядком права-вісімково» для файлів, що мають усі біти маски required."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print("\n".join(solve(sys.argv[1] if len(sys.argv) > 1 else ".", 0o111)))
