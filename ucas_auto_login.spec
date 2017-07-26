# -*- mode: python -*-

block_cipher = None


a = Analysis(['script\\gui.py'],
             pathex=['C:\\Users\\Cheer.L\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', '.\\script', 'C:\\Users\\Cheer.L\\Documents\\vs code\\py\\ucasAutolog'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ucas_auto_login',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='script\\ui\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='bin')
