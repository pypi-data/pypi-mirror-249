from setuptools import setup

name = "types-pluggy"
description = "Typing stubs for pluggy"
long_description = '''
## Typing stubs for pluggy

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pluggy`](https://github.com/pytest-dev/pluggy) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pluggy`.

This version of `types-pluggy` aims to provide accurate annotations
for `pluggy==1.2.0`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pluggy. All fixes for
types and metadata should be contributed there.

*Note:* The `pluggy` package includes type annotations or type stubs
since version 1.3.0. Please uninstall the `types-pluggy`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="1.2.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pluggy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pluggy-stubs'],
      package_data={'pluggy-stubs': ['__init__.pyi', '_hooks.pyi', '_manager.pyi', '_result.pyi', '_tracing.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
