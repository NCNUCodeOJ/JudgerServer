"""
define testcase of clang normal judge
"""
from typing import NoReturn

from testcase.base import BaseTestCase
from testcase.base import random_string
from service.judge import judge
from service.errors import CompileError

class Case(BaseTestCase):

    """
    define sub testcase of clang normal judge
    """

    clang_src = """#include <stdio.h>
int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d", a+b);
    return 0;
}"""

    def setUp(self) -> NoReturn:

        """
        set up the test case
        """

        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_clang_ac(self) -> NoReturn:

        """
        test clang ANSWER_CORRECT
        """

        judge_result = judge(
            self.clang_base_config, self.clang_src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 0)


    def test_clang_wa(self) -> NoReturn:

        """
        test clang WRONG_ANSWER
        """

        src = """#include <stdio.h>
int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d", a+b+1);
    return 0;
}"""

        judge_result = judge(
            self.clang_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_clang_tle(self) -> NoReturn:

        """
        test clang cpu time limit exceeded
        """

        src = """#include <stdio.h>
int main(){
    int a, b, h=2147483647, i;
    scanf("%d%d", &a, &b);
    printf("%d", a+b);
    for (i=0; i < h; i++)printf("%d", a+b);
    return 0;
}"""


        judge_result = judge(
            self.clang_base_config, src, 1, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 1)

    def test_clang_mle(self) -> NoReturn:

        """
        test clang memory limit exceeded
        """

        judge_result = judge(
            self.clang_base_config, self.clang_src, 1000, 1, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_clang_re(self) -> NoReturn:

        """
        test clang runtime error
        """

        src = """#include <stdio.h>
int main(){
    char a;
    scanf("%f", &a);
    printf("%f", a);
    return 1;
}"""

        judge_result = judge(
            self.clang_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 4)

    def test_clang_ce(self) -> NoReturn:

        """
        test clang compile error
        """

        src = """#include <stdio.h>
int main(){
    int a, b
    scanf("%d%d", &a, &b);
    printf("%d", a+b);
    return 0;
}"""

        try:
            judge(
                self.clang_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
            )
        except CompileError as exception:
            self.assertEqual(type(exception), CompileError)

    def test_clang_unicode(self) -> NoReturn:

        """
        test clang can run when have unicode strings
        """

        src = """#include <stdio.h>
int main(){
    char buf[80];
    scanf("%s", buf);
    printf("%s", buf);
    return 0;
}"""

        judge_result = judge(
            self.clang_base_config, src, 1000, 128*1024*1024, random_string(), "unicode",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 0)
