"""
1. test template class
2. base testcase
3. common use function

result return value
WRONG_ANSWER = -1
ANSWER_CORRECT = 0
CPU_TIME_LIMIT_EXCEEDED = 1
REAL_TIME_LIMIT_EXCEEDED = 2
MEMORY_LIMIT_EXCEEDED = 3
RUNTIME_ERROR = 4
SYSTEM_ERROR = 5

"""
import os
import shutil
import random
import string
import copy
from unittest import TestCase

from service.judge import judge
from service.errors import JudgeClientError
from .setting import _py3_lang_config
from .setting import _c_lang_config
from .setting import _cpp_lang_config
from .setting import _c_lang_spj_compile
from .setting import _c_lang_spj_config
from .setting import _java_lang_config

class BaseTestCase(TestCase):
    """
    test base class
    """
    BAD_SYSTEM_CALL = 31
    default_env = ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"]

    def init_workspace(self, language):

        """
        def init_workspace
        """

        base_workspace = "/tmp"
        workspace = os.path.join(base_workspace, language)
        shutil.rmtree(workspace, ignore_errors=True)
        os.makedirs(workspace)
        return workspace



    @property
    def py3_base_config(self):
        """return python3 base configuration"""
        return copy.deepcopy(_py3_lang_config)

    @property
    def clang_base_config(self):
        """return clang base configuration"""
        return copy.deepcopy(_c_lang_config)


    @property
    def cpp_base_config(self):
        """return clang base configuration"""
        return copy.deepcopy(_cpp_lang_config)

    @property
    def spj_clang_compile_base_config(self):
        """return c spj compile base configuration"""
        return copy.deepcopy(_c_lang_spj_compile)

    @property
    def spj_clang_base_config(self):
        """return c spj configuration"""
        return copy.deepcopy(_c_lang_spj_config)

    @property
    def java_base_config(self):
        """return java base configuration"""
        return copy.deepcopy(_java_lang_config)

def random_string():

    """
    Generate Random Strings
    """

    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(10))
class Case(BaseTestCase):

    """
    define base testcase
    """

    py3_src = "a, b = map(int,input().split())\nprint(a+b)"

    def setUp(self):
        """
        set up the test case
        """
        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_miss_test_case_id(self):

        """
        test if judge can detect missing test case id
        """

        try :
            judge(
                self.py3_base_config, self.py3_src, 1000, 128, "test1"
            )
        except JudgeClientError as exception:
            self.assertEqual(exception, "invalid parameter")
