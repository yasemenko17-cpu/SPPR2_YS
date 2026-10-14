from variants.variant_08 import solve

def test_empty_directory(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    res = solve(str(root))
    assert "Файлів: 0" in res
    assert "Каталогів: 0" in res
    assert "Символічних посилань: 0" in res
    assert "Найбільший: немає" in res

def test_only_symlink(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    target = tmp_path / "target.txt"
    target.write_text("hello")
    symlink = root / "link"
    symlink.symlink_to(target)
    
    res = solve(str(root))
    assert "Символічних посилань: 1" in res
    assert "Файлів: 0" in res

def test_multiple_files(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    
    file1 = root / "file1.txt"
    file1.write_text("abc")
    
    file2 = root / "file2.txt"
    file2.write_text("hello world")
    
    res = solve(str(root))
    assert "Файлів: 2" in res
    assert "Найбільший: file2.txt (11 байт)" in res