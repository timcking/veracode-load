# -*- mode: python -*-

block_cipher = None


a = Analysis(['LoadApp.py'],
             pathex=['C:\\proj\\veracode-load'],
             binaries=[],
             datas=[
			        ('C:\\proj\\veracode-load\\data\\Veracode.accdb', '.\\data\\'),
					('C:\\proj\\veracode-load\\run-loader.sh', '.'),
					('C:\\proj\\veracode-load\\README.*', '.'),
					('C:\\proj\\veracode-load\\VcParse.py', '.')
			       ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='LoadApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='LoadApp')
