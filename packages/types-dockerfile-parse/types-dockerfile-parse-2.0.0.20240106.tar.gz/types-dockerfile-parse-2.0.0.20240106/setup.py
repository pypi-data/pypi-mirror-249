from setuptools import setup

name = "types-dockerfile-parse"
description = "Typing stubs for dockerfile-parse"
long_description = '''
## Typing stubs for dockerfile-parse

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`dockerfile-parse`](https://github.com/containerbuildsystem/dockerfile-parse) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`dockerfile-parse`.

This version of `types-dockerfile-parse` aims to provide accurate annotations
for `dockerfile-parse==2.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/dockerfile-parse. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="2.0.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dockerfile-parse.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dockerfile_parse-stubs'],
      package_data={'dockerfile_parse-stubs': ['__init__.pyi', 'constants.pyi', 'parser.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
