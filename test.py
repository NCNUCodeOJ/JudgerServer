"""
import all testcase and run
"""
from unittest import main
from testcase.base          import Case as BaseCase
from testcase.spj_clang     import Case as SpjClangCase
from testcase.py3           import Case as Py3Case
from testcase.clang         import Case as ClangCase
from testcase.cpp           import Case as CppCase

if __name__ == '__main__':
    main()
