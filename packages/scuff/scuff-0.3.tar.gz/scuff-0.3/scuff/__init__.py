'''
Scuff:
    A data serialization language and transpiler suite written in Python.
'''


__title__ = 'scuff'
__description__ = "A config file format and transpiler suite written in Python."
__url__ = "https://github.com/akyuute/scuff"
__version__ = '0.3'
__author__ = "akyuute"
__license__ = 'MIT'
__copyright__ = "Copyright (c) 2023-present akyuute"


ENDMARKER = ''
NEWLINE = '\n'
KEYWORDS = ()


from .tools import (
    ast_to_py,
    dump,
    file_to_py,
    parse,
    py_to_scuff,
    scuff_to_py,
    unparse,
)
from .parser import (
    FileParser,
    RecursiveDescentParser,
    PyParser,
    Unparser,
)
from .compiler import Compiler

