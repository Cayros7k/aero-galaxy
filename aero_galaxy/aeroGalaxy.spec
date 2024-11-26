# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['aeroGalaxy.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/backgrounds', 'assets/backgrounds'), ('assets/bullets', 'assets/bullets'), ('assets/explosions', 'assets/explosions'), ('assets/meteors', 'assets/meteors'), ('assets/player', 'assets/player'), ('assets/powerups', 'assets/powerups'), ('sounds', 'sounds')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='aeroGalaxy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
