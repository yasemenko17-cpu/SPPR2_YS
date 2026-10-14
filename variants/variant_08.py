import os
import stat

def solve(root: str) -> str:
    """
    Підсумковий звіт про дерево каталогів (Варіант 23, набір В).
    """
    file_count = 0
    dir_count = 0
    symlink_count = 0
    total_size = 0
    seen_inodes = set()
    
    largest_path = None
    largest_size = -1

    for current_root, dirs, files in os.walk(root, followlinks=False):
        # Рахуємо каталоги без самого root
        if os.path.abspath(current_root) != os.path.abspath(root):
            dir_count += 1
        
        try:
            entries = os.listdir(current_root)
        except OSError:
            entries = []

        for entry in entries:
            full_path = os.path.join(current_root, entry)
            rel_path = os.path.relpath(full_path, root)
            try:
                st = os.lstat(full_path)
            except OSError:
                continue

            if stat.S_ISLNK(st.st_mode):
                symlink_count += 1
            elif stat.S_ISREG(st.st_mode):
                file_count += 1
                inode_key = (st.st_dev, st.st_ino)
                # Жорсткі посилання на один файл враховують розмір один раз
                if inode_key not in seen_inodes:
                    seen_inodes.add(inode_key)
                    total_size += st.st_size
                
                # Пошук найбільшого файла
                if st.st_size > largest_size:
                    largest_size = st.st_size
                    largest_path = rel_path
                elif st.st_size == largest_size:
                    if largest_path is None or rel_path < largest_path:
                        largest_path = rel_path

    if largest_path is None:
        largest_str = "Найбільший: немає"
    else:
        largest_str = f"Найбільший: {largest_path} ({largest_size} байт)"

    result_lines = [
        f"Файлів: {file_count}",
        f"Каталогів: {dir_count}",
        f"Символічних посилань: {symlink_count}",
        f"Загальний розмір: {total_size} байт",
        largest_str
    ]
    return "\n".join(result_lines)