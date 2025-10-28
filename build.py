import PyInstaller.__main__

PyInstaller.__main__.run([
    '--hidden-import=torch',
    '--hidden-import=torchvision',
    '--collect-submodules=torch',
    '--collect-submodules=torchvision',
    '--collect-data=torch',
    '--collect-data=torchvision',
    '-i', 'icon.png',
    '-n', 'Enhanced Local Photo Search',
    '--windowed',
    'main.py',
])