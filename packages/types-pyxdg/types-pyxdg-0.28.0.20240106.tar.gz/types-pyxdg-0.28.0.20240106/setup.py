from setuptools import setup

name = "types-pyxdg"
description = "Typing stubs for pyxdg"
long_description = '''
## Typing stubs for pyxdg

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyxdg`](https://github.com/takluyver/pyxdg) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyxdg`.

This version of `types-pyxdg` aims to provide accurate annotations
for `pyxdg==0.28.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyxdg. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="0.28.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyxdg.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['xdg-stubs'],
      package_data={'xdg-stubs': ['BaseDirectory.pyi', 'Config.pyi', 'DesktopEntry.pyi', 'Exceptions.pyi', 'IconTheme.pyi', 'IniFile.pyi', 'Locale.pyi', 'Menu.pyi', 'MenuEditor.pyi', 'Mime.pyi', 'RecentFiles.pyi', '__init__.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
