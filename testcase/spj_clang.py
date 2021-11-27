"""
define testcase of C base spj
"""
from typing import NoReturn

from testcase.base import BaseTestCase
from testcase.base import random_string
from service.errors import SPJCompileError
from service.judge import judge
from service.judge import compile_spj

class Case(BaseTestCase):

    """
    define sub testcase of C base spj
    """

    spj_src_ac = "#include <stdio.h>\nint main(){\n\treturn 0;\n}"
    spj_src_wa = "#include <stdio.h>\nint main(){\n\treturn 1;\n}"
    spj_src = spj_src_ac
    py3_src = "a, b = map(int,input().split())\nprint(a+b)"

    def setUp(self) -> NoReturn:

        """
        set up the test case
        """

        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_spj_clang_compile_success(self) -> NoReturn:

        """
        test if spj compilation is success
        """

        try:
            result = compile_spj(random_string(), self.spj_src, self.spj_clang_compile_base_config)
            self.assertEqual(result, "success")
        except SPJCompileError as exception:
            print(exception.message)
            self.assertEqual(type(exception), None)

    def test_spj_clang_compile_error(self) -> NoReturn:

        """
        test if spj compilation can raise SPJCompileError
        """

        c_spj_src = "#include <stdio.h>\nint main(){\n\treturn 1;]\n}"

        try:
            compile_spj(random_string(), c_spj_src, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

    def test_spj_clang_ac(self) -> NoReturn:

        """
        test if spj can detect ANSWER_CORRECT
        """

        version = random_string()

        try:
            compile_spj(version, self.spj_src_ac, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1000, 128*1024*1024, random_string(), "spj",
            spj_version=version, spj_config=self.spj_clang_base_config,
            spj_compile_config=self.spj_clang_compile_base_config, spj_src=self.spj_src
        )

        for result in judge_result:
            self.assertEqual(result["result"], 0)

    def test_spj_clang_wa(self) -> NoReturn:

        """
        test if spj can detect WRONG_ANSWER
        """

        version = random_string()

        try:
            compile_spj(version, self.spj_src_wa, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1000, 128*1024*1024, random_string(), "spj",
            spj_version=version, spj_config=self.spj_clang_base_config,
            spj_compile_config=self.spj_clang_compile_base_config, spj_src=self.spj_src
        )

        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_spj_clang_tle(self) -> NoReturn:

        """
        test if spj can detect cpu time limit exceeded
        """

        version = random_string()

        try:
            compile_spj(version, self.spj_src_ac, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1, 128*1024*1024, random_string(), "spj",
            spj_version=version, spj_config=self.spj_clang_base_config,
            spj_compile_config=self.spj_clang_compile_base_config, spj_src=self.spj_src
        )

        for result in judge_result:
            self.assertEqual(result["result"], 1)

    def test_spj_clang_mle(self) -> NoReturn:

        """
        test if spj can detect memory limit exceeded
        """

        version = random_string()

        try:
            compile_spj(version, self.spj_src_ac, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

        judge_result = judge(
            self.py3_base_config, self.py3_src, 1000, 1, random_string(), "spj",
            spj_version=version, spj_config=self.spj_clang_base_config,
            spj_compile_config=self.spj_clang_compile_base_config, spj_src=self.spj_src
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_spj_clang_re(self) -> NoReturn:

        """
        test if spj can detect runtime error
        """

        version = random_string()
        src = "a = map(int,input().split())\nprint(a+b)"

        try:
            compile_spj(version, self.spj_src_ac, self.spj_clang_compile_base_config)
        except SPJCompileError as exception:
            self.assertEqual(type(exception), SPJCompileError)

        judge_result = judge(
            self.py3_base_config, src, 1000, 1, random_string(), "spj",
            spj_version=version, spj_config=self.spj_clang_base_config,
            spj_compile_config=self.spj_clang_compile_base_config, spj_src=self.spj_src
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)
