from setuptools import setup, Extension

_pymovex3 = Extension("_pymovex3", sources=["_pymovex3.c"], libraries=["MvxSock"])

setup(
    name="pymovex3",
    version="1.1.0.1",
    description="Python module for interacting with M3/Movex, implemented using the C-API",
    py_modules=["pymovex3"],
    ext_modules=[_pymovex3],
    author="Jean-Baptiste Quenot, Ludovico Maria Ottaviani",
    author_email="me@ludovicoottaviani.eu",
    url="https://github.com/Lyut/pymovex3",
)
