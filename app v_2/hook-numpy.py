from PyInstaller.utils.hooks import copy_metadata, collect_submodules

datas = copy_metadata('numpy')
hiddenimports = collect_submodules('numpy')
