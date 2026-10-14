def solve(root):
    """Повертає групи шляхів звичайних файлів, що є жорсткими посиланнями на один inode."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print(solve(sys.argv[1] if len(sys.argv) > 1 else "."))
