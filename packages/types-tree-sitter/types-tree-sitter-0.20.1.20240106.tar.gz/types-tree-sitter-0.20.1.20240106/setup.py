from setuptools import setup

name = "types-tree-sitter"
description = "Typing stubs for tree-sitter"
long_description = '''
## Typing stubs for tree-sitter

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`tree-sitter`](https://github.com/tree-sitter/py-tree-sitter) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`tree-sitter`.

This version of `types-tree-sitter` aims to provide accurate annotations
for `tree-sitter==0.20.1`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tree-sitter. All fixes for
types and metadata should be contributed there.

*Note:* The `tree-sitter` package includes type annotations or type stubs
since version 0.20.3. Please uninstall the `types-tree-sitter`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="0.20.1.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tree-sitter.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['tree_sitter-stubs'],
      package_data={'tree_sitter-stubs': ['__init__.pyi', 'binding.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
