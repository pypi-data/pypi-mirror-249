from setuptools import setup

name = "types-pyOpenSSL"
description = "Typing stubs for pyOpenSSL"
long_description = '''
## Typing stubs for pyOpenSSL

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyOpenSSL`](https://github.com/pyca/pyopenssl) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyOpenSSL`.

This version of `types-pyOpenSSL` aims to provide accurate annotations
for `pyOpenSSL==23.3.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyOpenSSL. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="23.3.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyOpenSSL.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['cryptography>=35.0.0'],
      packages=['OpenSSL-stubs'],
      package_data={'OpenSSL-stubs': ['SSL.pyi', '__init__.pyi', 'crypto.pyi', 'rand.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
