#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path


def pargs() -> None:
    global args
    parser = argparse.ArgumentParser(
        description='fntファイルの高さのパラメータを変更する')
    parser.add_argument('-y', type=int, default=0, help='yの変更値')
    parser.add_argument('-t', type=int, default=0, help='heightの変更値')
    parser.add_argument('files', nargs='+', help='1つ以上の入力ファイル')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()


def process():
    for file in args.files:
        fp = Path(file)
        text = fp.read_text(encoding='utf-8')
        lines = text.splitlines()
        # 3行目から処理する
        i: int = 2
        iMax: int = len(lines)
        while(i < iMax):
            m = re.search(r'^(.+\sy=)(\d+)(\s.+\sheight=)(\d+)(\s.+)$', lines[i])
            if not m:
                continue
            y = int(m.group(2)) + args.y
            h = int(m.group(4)) + args.t
            lines[i] = ''.join([m.group(1), str(y), m.group(3), str(h), m.group(5)])
        text = '\n'.join(lines)
        fp.write_text(text, encoding='utf-8')


def main():
    pargs()
    process()
    return 0


if __name__ == '__main__':
    # MSYS2での文字化け対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.exit(main())
