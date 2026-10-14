def solve(root):
    """Повертає рядки «шлях -> ціль [ok|broken]» для всіх символічних посилань дерева."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print("\n".join(solve(sys.argv[1] if len(sys.argv) > 1 else ".")))
