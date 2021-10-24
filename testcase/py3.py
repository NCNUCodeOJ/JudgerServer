"""
define testcase of python3 normal judge
"""
from typing import NoReturn

from testcase.base import BaseTestCase
from testcase.base import random_string
from service.judge import judge
from service.errors import CompileError

class Case(BaseTestCase):

    """
    define sub testcase of python3 normal judge
    """

    py3_src = "a, b = map(int,input().split())\nprint(a+b)"

    def setUp(self) -> NoReturn:

        """
        set up the test case
        """

        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_py3_ac(self) -> NoReturn:

        """
        test py3 ANSWER_CORRECT
        """

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 0)


    def test_py3_wa(self) -> NoReturn:

        """
        test py3 WRONG_ANSWER
        """

        src = "a, b = map(int,input().split())\nprint(a+b+1)"

        judge_result = judge(
            self.py3_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_py3_tle(self) -> NoReturn:

        """
        test py3 cpu time limit exceeded
        """

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 1)

    def test_py3_mle(self) -> NoReturn:

        """
        test py3 memory limit exceeded
        """

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1000, 1, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_py3_re(self) -> NoReturn:

        """
        test py3 runtime error
        """

        src = "a = map(int,input().split())\nprint(a+b)"

        judge_result = judge(
            self.py3_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 4)

    def test_py3_ce(self) -> NoReturn:

        """
        test py3 compile error
        """

        src = "a, b = map(int,input().split())\n\tprint(a+b)"

        try:
            judge(
                self.py3_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
            )
        except CompileError as exception:
            self.assertEqual(type(exception), CompileError)

    def test_py3_unicode(self) -> NoReturn:

        """
        test py3 can run when have unicode strings
        """

        src = "print(input())"

        judge_result = judge(
            self.py3_base_config, src, 1000, 128*1024*1024, random_string(), "unicode",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 0)