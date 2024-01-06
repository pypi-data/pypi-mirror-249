from setuptools import setup

name = "types-python-dateutil"
description = "Typing stubs for python-dateutil"
long_description = '''
## Typing stubs for python-dateutil

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-dateutil`](https://github.com/dateutil/dateutil) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-dateutil`.

This version of `types-python-dateutil` aims to provide accurate annotations
for `python-dateutil==2.8.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-dateutil. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="2.8.19.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-dateutil.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateutil-stubs'],
      package_data={'dateutil-stubs': ['__init__.pyi', '_common.pyi', 'easter.pyi', 'parser/__init__.pyi', 'parser/isoparser.pyi', 'relativedelta.pyi', 'rrule.pyi', 'tz/__init__.pyi', 'tz/_common.pyi', 'tz/tz.pyi', 'utils.pyi', 'zoneinfo/__init__.pyi', 'zoneinfo/rebuild.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
