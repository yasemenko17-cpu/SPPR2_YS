"""Відкриті приклади з карток: по три набори даних для кожної з десяти задач. Повні тести — у викладача."""
import os
import stat

import pytest
from conftest import fill, load, make_tree, open_fds

DATA = {1: {'sets': [{'label': 'A',
               'tree': [('d', 'src/util'),
                        ('d', 'logs'),
                        ('f', 'src/main.py', 120, {}),
                        ('f', 'src/util/io.py', 40, {}),
                        ('f', 'src/util/net.py', 300, {}),
                        ('f', 'README.md', 500, {}),
                        ('f', 'logs/app.log', 2000, {}),
                        ('f', 'logs/old.log', 10, {}),
                        ('l', 'src/link.py', 'main.py')],
               'args': ['@root', '.py', 100, None],
               'expected': ['src/main.py', 'src/util/net.py']},
              {'label': 'B',
               'tree': [('f', 'logs/a.log', 5, {'mtime': 1700000200}),
                        ('f', 'logs/b.log', 0, {'mtime': 1700000100}),
                        ('f', 'logs/c.log', 7, {'mtime': 1700000099}),
                        ('f', 'logs/deep/d.log', 9, {'mtime': 1700000500}),
                        ('f', 'logs/e.txt', 50, {'mtime': 1700000900}),
                        ('d', 'logs/dir.log')],
               'args': ['@root', '.log', 0, 1700000100],
               'expected': ['logs/a.log', 'logs/b.log', 'logs/deep/d.log']},
              {'label': 'C',
               'tree': [('f', 'a.TXT', 3, {}),
                        ('f', 'b.txt', 3, {}),
                        ('f', 'c.TXT', 0, {}),
                        ('f', 'sub/d.TXT', 1, {}),
                        ('f', '.hidden.TXT', 5, {})],
               'args': ['@root', '.TXT', 1, None],
               'expected': ['.hidden.TXT', 'a.TXT', 'sub/d.TXT']}],
     'edges': []},
 2: {'sets': [{'label': 'A',
               'tree': [('f', 'run.sh', 1, {'mode': 493}),
                        ('f', 'tool', 1, {'mode': 488}),
                        ('f', 'data.txt', 1, {'mode': 420}),
                        ('f', 'bin/app', 1, {'mode': 457}),
                        ('f', 'bin/ro', 1, {'mode': 292})],
               'args': ['@root', 73],
               'expected': ['bin/app -rwx--x--x 0711', 'run.sh -rwxr-xr-x 0755']},
              {'label': 'B',
               'tree': [('f', 'a', 1, {'mode': 384}),
                        ('f', 'b', 1, {'mode': 420}),
                        ('f', 'c', 1, {'mode': 256}),
                        ('f', 'd', 1, {'mode': 438}),
                        ('f', 'sub/e', 1, {'mode': 493})],
               'args': ['@root', 384],
               'expected': ['a -rw------- 0600', 'b -rw-r--r-- 0644', 'd -rw-rw-rw- 0666', 'sub/e -rwxr-xr-x 0755']},
              {'label': 'C',
               'tree': [('f', 'su', 1, {'mode': 2541}),
                        ('f', 'plain', 1, {'mode': 493}),
                        ('f', 'x', 1, {'mode': 2468}),
                        ('f', 'g', 1, {'mode': 1517})],
               'args': ['@root', 2048],
               'expected': ['su -rwsr-xr-x 4755', 'x -rwSr--r-- 4644']}],
     'edges': []},
 3: {'sets': [{'label': 'A',
               'tree': [('f', 'a.txt', 1, {}),
                        ('l', 'ln1', 'a.txt'),
                        ('l', 'ln2', 'missing.txt'),
                        ('d', 'sub'),
                        ('l', 'sub/up', '../a.txt')],
               'args': ['@root'],
               'expected': ['ln1 -> a.txt [ok]', 'ln2 -> missing.txt [broken]', 'sub/up -> ../a.txt [ok]']},
              {'label': 'B',
               'tree': [('f', 'data/x', 1, {}),
                        ('l', 'shortcut', 'data'),
                        ('l', 'data/loop-out', '../nothing'),
                        ('l', 'chain', 'shortcut')],
               'args': ['@root'],
               'expected': ['chain -> shortcut [ok]', 'data/loop-out -> ../nothing [broken]', 'shortcut -> data [ok]']},
              {'label': 'C',
               'tree': [('f', 'a', 1, {}), ('d', 'x/y'), ('l', 'x/y/z', '../../a'), ('l', 'w', 'x/y/zz')],
               'args': ['@root'],
               'expected': ['w -> x/y/zz [broken]', 'x/y/z -> ../../a [ok]']}],
     'edges': []},
 4: {'sets': [{'label': 'A',
               'tree': [('f', 'a', 5, {}), ('h', 'b', 'a'), ('h', 'sub/c', 'a'), ('f', 'd', 3, {})],
               'args': ['@root'],
               'expected': [['a', 'b', 'sub/c']]},
              {'label': 'B',
               'tree': [('f', 'x', 1, {}), ('h', 'y', 'x'), ('f', 'm', 2, {}), ('h', 'n', 'm'), ('h', 'k/n2', 'm'), ('f', 'solo', 3, {})],
               'args': ['@root'],
               'expected': [['k/n2', 'm', 'n'], ['x', 'y']]},
              {'label': 'C',
               'tree': [('f', '../ext.txt', 4, {}), ('h', 'only.txt', '../ext.txt'), ('f', 'p', 1, {}), ('h', 'q', 'p'), ('l', 'sl', 'p')],
               'args': ['@root'],
               'expected': [['p', 'q']]}],
     'edges': []},
 5: {'sets': [{'label': 'A', 'tree': [], 'args': ['@root/out.txt', ['alpha', 'beta'], False], 'expected': [11, b'alpha\nbeta\n']},
              {'label': 'B',
               'tree': [('f', 'out.txt', b'old\n', {})],
               'args': ['@root/out.txt', ['new'], True],
               'expected': [4, b'old\nnew\n']},
              {'label': 'C',
               'tree': [('f', 'out.txt', b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', {})],
               'args': ['@root/out.txt', ['Привіт', 'світ'], False],
               'expected': [22, b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd1\x96\xd1\x82\n\xd1\x81\xd0\xb2\xd1\x96\xd1\x82\n']}],
     'edges': []},
 6: {'sets': [{'label': 'A',
               'tree': [('f', 'data.bin', b'0123456789', {})],
               'args': ['@root/data.bin', [('a', 3), ('b', 3), ('c', 3), ('a', 2)]],
               'expected': ['012', '345', '012', '67']},
              {'label': 'B',
               'tree': [('f', 'data.bin', b'abcdefghij', {})],
               'args': ['@root/data.bin', [('c', 4), ('c', 4), ('b', 2), ('a', 2), ('c', 4)]],
               'expected': ['abcd', 'efgh', 'ab', 'cd', 'ij']},
              {'label': 'C',
               'tree': [('f', 'data.bin', b'xyz', {})],
               'args': ['@root/data.bin', [('b', 10), ('a', 1), ('c', 2), ('c', 5)]],
               'expected': ['xyz', '', 'xy', 'z']}],
     'edges': []},
 7: {'sets': [{'label': 'A',
               'tree': [('f', 'a.txt', 5, {}), ('d', 'dir')],
               'args': ['@root', ['a.txt', 'dir', 'nofile', 'a.txt/x']],
               'expected': ['a.txt: ok', 'dir: EISDIR', 'nofile: ENOENT', 'a.txt/x: ENOTDIR']},
              {'label': 'B',
               'tree': [('f', 'e.txt', 0, {}), ('l', 'ln', 'e.txt'), ('l', 'dang', 'nothing')],
               'args': ['@root', ['ln', 'dang', 'e.txt', 'dang/x']],
               'expected': ['ln: ELOOP', 'dang: ELOOP', 'e.txt: ok', 'dang/x: ENOENT']},
              {'label': 'C',
               'tree': [('d', 'd1/d2'), ('f', 'd1/f', 1, {})],
               'args': ['@root', ['d1/d2', 'd1/f/', 'd1/f/z', 'd1', 'd1/../d1/f']],
               'expected': ['d1/d2: EISDIR', 'd1/f/: ENOTDIR', 'd1/f/z: ENOTDIR', 'd1: EISDIR', 'd1/../d1/f: ok']}],
     'edges': []},
 8: {'sets': [{'label': 'A',
               'tree': [('f', 'a', 10, {}), ('f', 'd1/b', 30, {}), ('f', 'd1/d2/c', 20, {}), ('d', 'empty')],
               'args': ['@root'],
               'expected': 'Файлів: 3\nКаталогів: 3\nСимволічних посилань: 0\nЗагальний розмір: 60 байт\nНайбільший: d1/b (30 байт)'},
              {'label': 'B',
               'tree': [('f', 'x', 100, {}), ('h', 'y', 'x'), ('f', 'z', 40, {}), ('l', 's', 'x')],
               'args': ['@root'],
               'expected': 'Файлів: 3\nКаталогів: 0\nСимволічних посилань: 1\nЗагальний розмір: 140 байт\nНайбільший: x (100 байт)'},
              {'label': 'C',
               'tree': [('f', 'a/f', 0, {}), ('l', 'la', 'a')],
               'args': ['@root'],
               'expected': 'Файлів: 1\nКаталогів: 1\nСимволічних посилань: 1\nЗагальний розмір: 0 байт\nНайбільший: a/f (0 байт)'}],
     'edges': []},
 9: {'sets': [{'label': 'A', 'tree': [('f', 'log.txt', b'l1\nl2\nl3\nl4\n', {})], 'args': ['@root/log.txt', 2], 'expected': ['l3', 'l4']},
              {'label': 'B', 'tree': [('f', 'log.txt', b'a\nbb\nccc', {})], 'args': ['@root/log.txt', 2], 'expected': ['bb', 'ccc']},
              {'label': 'C',
               'tree': [('f', 'log.txt', b'\xd0\x9e\xd0\xb4\xd0\xb8\xd0\xbd\n\xd0\x94\xd0\xb2\xd0\xb0\n\xd0\xa2\xd1\x80\xd0\xb8\n', {})],
               'args': ['@root/log.txt', 5],
               'expected': ['Один', 'Два', 'Три']}],
     'edges': []},
 10: {'sets': [{'label': 'A', 'tree': [('d', 'etc')], 'args': ['@root/etc/conf.ini', b'hello', 420], 'expected': [5, b'hello', 420]},
               {'label': 'B',
                'tree': [('f', 'conf.ini', b'old-config\n', {'mode': 384})],
                'args': ['@root/conf.ini', b'new\n', 384],
                'expected': [4, b'new\n', 384]},
               {'label': 'C',
                'tree': [('f', 'app/settings.cfg', b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', {'mode': 511})],
                'args': ['@root/app/settings.cfg',
                         b'\xd0\x9d\xd0\xb0\xd0\xbb\xd0\xb0\xd1\x88\xd1\x82\xd1\x83\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xbd\xd1\x8f\n',
                         416],
                'expected': [25,
                             b'\xd0\x9d\xd0\xb0\xd0\xbb\xd0\xb0\xd1\x88\xd1\x82\xd1\x83\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xbd\xd1\x8f\n',
                             416]}],
      'edges': []}}


def cases(include_edges):
    out = []
    for number, task in DATA.items():
        for index, case in enumerate(task["sets"]):
            out.append(pytest.param(number, case, id=f"v{3 * (number - 1) + index + 1:02d}"))
        if include_edges:
            for index, case in enumerate(task.get("edges", []), 1):
                out.append(pytest.param(number, case, id=f"t{number:02d}-крайній-{index}"))
    return out


def build(tmp_path, case):
    root = tmp_path / "data"
    make_tree(root, case["tree"])
    return root, fill(case["args"], root)


def check_pure(number, case, tmp_path):
    root, args = build(tmp_path, case)
    assert load(number).solve(*args) == case["expected"]


def check_redirect(case, tmp_path, capfd):
    root, args = build(tmp_path, case)
    expected_ret, expected_bytes = case["expected"]
    ret = load(5).solve(*args)
    assert ret == expected_ret
    assert open(args[0], "rb").read() == expected_bytes
    os.write(1, b"stdout works\n")
    assert capfd.readouterr().out == "stdout works\n"  # у файл нічого зайвого, а дескриптор 1 відновлено


def check_atomic(case, tmp_path):
    root, args = build(tmp_path, case)
    path = args[0]
    directory = os.path.dirname(path)
    before = set(os.listdir(directory))
    old_ino = os.stat(path).st_ino if os.path.exists(path) else None
    old_fd = os.open(path, os.O_RDONLY) if old_ino is not None else None
    old_content = os.read(old_fd, 1000) if old_fd is not None else None
    expected_ret, expected_bytes, expected_mode = case["expected"]
    try:
        ret = load(10).solve(*args)
        assert ret == expected_ret
        with open(path, "rb") as handle:
            assert handle.read() == expected_bytes
        assert stat.S_IMODE(os.stat(path).st_mode) == expected_mode
        assert set(os.listdir(directory)) == before | {os.path.basename(path)}
        if old_ino is not None:
            assert os.stat(path).st_ino != old_ino  # rename підставив новий inode
            os.lseek(old_fd, 0, os.SEEK_SET)
            assert os.read(old_fd, 1000) == old_content  # старий дескриптор бачить старий вміст
    finally:
        if old_fd is not None:
            os.close(old_fd)


def run_case(number, case, tmp_path, capfd):
    if number == 5:
        check_redirect(case, tmp_path, capfd)
    elif number == 10:
        check_atomic(case, tmp_path)
    else:
        check_pure(number, case, tmp_path)



@pytest.mark.parametrize("number,case", cases(False))
def test_приклади_з_картки(number, case, tmp_path, capfd):
    """Відкриті приклади: по три набори даних для кожної задачі (запускайте лише свій: pytest -k v13)."""
    run_case(number, case, tmp_path, capfd)
