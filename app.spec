# -*- mode: python ; coding: utf-8 -*-
import os

spec_root = os.path.abspath('.')

block_cipher = None


a = Analysis([os.path.join(spec_root, 'app.py')],
             pathex=[spec_root],
             binaries=[],
             datas=[],
             hiddenimports=['PySide2.QtXml', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += Tree(os.path.join(spec_root, 'lib'), prefix='lib', excludes=["*.py", "*.pyc", "*.qrc", "*.bat"])
a.datas += Tree(os.path.join(spec_root, 'env', 'Lib', 'site-packages', 'qt_material'), prefix='qt_material', excludes=["*.py", "*.pyc", "*.qrc", "*.bat"])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TriangleAdjacencyMatrix',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon=os.path.join(spec_root, 'icon.ico'))
