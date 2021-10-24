"""
define testcase of cpp normal judge
"""
from typing import NoReturn

from testcase.base import BaseTestCase
from testcase.base import random_string
from service.judge import judge
from service.errors import CompileError

class Case(BaseTestCase):

    """
    define sub testcase of cpp normal judge
    """

    cpp_src = """#include <iostream>
int main() {
  int a, b;
  std::cin>> a >> b;
  std::cout << a + b;
  return 0;
}"""

    def setUp(self) -> NoReturn:

        """
        set up the test case
        """

        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_cpp_ac(self) -> NoReturn:

        """
        test cpp ANSWER_CORRECT
        """

        judge_result = judge(
            self.cpp_base_config, self.cpp_src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 0)


    def test_cpp_wa(self) -> NoReturn:

        """
        test cpp WRONG_ANSWER
        """

        src = """#include <iostream>
int main() {
  int a, b;
  std::cin>> a >> b;
  std::cout << a + b + 1;
  return 0;
}"""

        judge_result = judge(
            self.cpp_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_cpp_tle(self) -> NoReturn:

        """
        test cpp cpu time limit exceeded
        """

        src = """#include <iostream>
int main() {
  int a, b;
  std::cin>> a >> b;
  for(int i = 0; i < 2147483647; i++)
  std::cout << a + b;
  return 0;
}"""


        judge_result = judge(
            self.cpp_base_config, src, 1, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 1)

    def test_cpp_mle(self) -> NoReturn:

        """
        test cpp memory limit exceeded
        """

        judge_result = judge(
            self.cpp_base_config, self.cpp_src, 1000, 1, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_cpp_re(self) -> NoReturn:

        """
        test cpp runtime error
        """

        src = """#include <iostream>
int main() {
  int a, b;
  std::cin>> a >> b;
  std::cout << a + b;
  return 1;
}"""

        judge_result = judge(
            self.cpp_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 4)

    def test_cpp_ce(self) -> NoReturn:

        """
        test cpp compile error
        """

        src = """#include <iostream>
int main() {
  int a, b
  std::cin>> a >> b;
  std::cout << a + b;
  return 0;
}"""

        try:
            judge(
                self.cpp_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
            )
        except CompileError as exception:
            self.assertEqual(type(exception), CompileError)

    def test_cpp_unicode(self) -> NoReturn:

        """
        test cpp can run when have unicode strings
        """

        src = """#include <iostream>
#include <cstring>
int main() {
  std::string a;
  std::cin>> a;
  std::cout << a;
  return 0;
}"""

        judge_result = judge(
            self.cpp_base_config, src, 1000, 128*1024*1024, random_string(), "unicode",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 0)
