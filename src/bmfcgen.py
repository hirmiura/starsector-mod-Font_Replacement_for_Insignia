#!/usr/bin/env -S python3
# SPDX-License-Identifier: MIT
# Copyright 2022 hirmiura <https://github.com/hirmiura>
#
# 使い方
# $ENV:Path="bmfont.exeのパス;"+$ENV:Path
# bmfcgen.py
# のんびり待つ
from __future__ import annotations

import io
import os
import pathlib
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

from BMFC import BMFC

BMFONT_EXE = 'bmfont64.exe'
DST_DIR = '../mod/graphics/fonts/'
SRC_DIR = pathlib.Path(__file__).parent
BMFC_TEMP_FILE = 'bmfc_template.txt'


@dataclass
class TextureSize:
    Width: int
    Height: int


@dataclass
class BmfGenConf(BMFC):
    outputfile: str = ''
    nameInStarsector: list[str] = field(default_factory=list)

    @property
    def bmfc_file(self):
        return self.outputfile + '.bmfc'

    @property
    def fnt_file(self):
        return self.outputfile + '.fnt'

    @property
    def png_file(self):
        return self.outputfile + '_0.png'


bmf_config = [
    BmfGenConf(outputfile='Sika15aa', fontName='Cica', fontFile='Cica-Regular.otf',
               fontSize=-15, aa=4, renderFromOutline=0,
               outWidth=4096, outHeight=2048, nameInStarsector=['insignia15LTaa']),

    BmfGenConf(outputfile='Sika21aa', fontName='Cica', fontFile='Cica-Regular.otf',
               fontSize=-21, aa=4, renderFromOutline=0,
               outWidth=4096, outHeight=4096, nameInStarsector=['insignia21LTaa']),

    BmfGenConf(outputfile='Sika25aa', fontName='Cica', fontFile='Cica-Regular.otf',
               fontSize=-25, aa=4, renderFromOutline=0,
               outWidth=4096, outHeight=4096, nameInStarsector=['insignia25LTaa']),
]


def init_config():
    temp = BMFC.load(BMFC_TEMP_FILE)
    for c in bmf_config:
        c.chars = temp.chars


def generate_bmfc():
    print('bmfcファイルを生成中...', flush=True)
    count: int = 0
    for conf in bmf_config:
        count += 1
        conf.save(conf.bmfc_file)
        print('==>' + conf.bmfc_file, flush=True)
    print(f'{count} ファイル生成完了', flush=True)


def generate_font():
    print('ビットマップフォントを生成中...', flush=True)
    count: int = 0
    for conf in bmf_config:
        count += 1
        print('==>' + conf.fnt_file, flush=True)
        com = [BMFONT_EXE, '-c', conf.bmfc_file, '-o', conf.fnt_file]
        subprocess.run(com, shell=True)
    print(f'{count} フォント生成完了', flush=True)


def install():
    print('生成したファイルをインストール中...', flush=True)
    for conf in bmf_config:
        print('==>' + conf.outputfile, flush=True)
        print(f'Move {conf.png_file} to {DST_DIR}{conf.png_file}', flush=True)
        shutil.move(conf.png_file, DST_DIR + conf.png_file)
        for fnt in conf.nameInStarsector:
            print(f'Copy {conf.fnt_file} to {DST_DIR}{fnt}.fnt', flush=True)
            shutil.copy2(conf.fnt_file, DST_DIR + fnt + '.fnt')
        print(f'Remove {conf.fnt_file}', flush=True)
        os.remove(conf.fnt_file)
    print('インストール完了', flush=True)


def main():
    print('bmfcgen.py', flush=True)

    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean()
        return 0

    init_config()
    generate_bmfc()
    print()
    generate_font()
    print()
    install()
    return 0


def clean():
    print('ファイルを削除...', flush=True)
    subprocess.run(['del', '*.bmfc'], shell=True)
    subprocess.run(['del', '*.fnt'], shell=True)
    subprocess.run(['del', '*.png'], shell=True)


if __name__ == '__main__':
    # MSYS2での文字化け対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.exit(main())
