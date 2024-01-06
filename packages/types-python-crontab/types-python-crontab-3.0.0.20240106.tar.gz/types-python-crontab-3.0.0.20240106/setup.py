from setuptools import setup

name = "types-python-crontab"
description = "Typing stubs for python-crontab"
long_description = '''
## Typing stubs for python-crontab

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-crontab`](https://gitlab.com/doctormo/python-crontab) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-crontab`.

This version of `types-python-crontab` aims to provide accurate annotations
for `python-crontab==3.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-crontab. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="3.0.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-crontab.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['crontabs-stubs', 'cronlog-stubs', 'crontab-stubs'],
      package_data={'crontabs-stubs': ['__init__.pyi', 'METADATA.toml'], 'cronlog-stubs': ['__init__.pyi', 'METADATA.toml'], 'crontab-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
