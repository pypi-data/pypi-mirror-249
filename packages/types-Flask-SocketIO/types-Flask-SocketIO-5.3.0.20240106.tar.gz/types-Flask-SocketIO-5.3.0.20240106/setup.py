from setuptools import setup

name = "types-Flask-SocketIO"
description = "Typing stubs for Flask-SocketIO"
long_description = '''
## Typing stubs for Flask-SocketIO

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Flask-SocketIO`](https://github.com/miguelgrinberg/flask-socketio) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Flask-SocketIO`.

This version of `types-Flask-SocketIO` aims to provide accurate annotations
for `Flask-SocketIO==5.3.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Flask-SocketIO. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="5.3.0.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-SocketIO.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Flask>=0.9'],
      packages=['flask_socketio-stubs'],
      package_data={'flask_socketio-stubs': ['__init__.pyi', 'namespace.pyi', 'test_client.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
