"""
define testcase of java normal judge
"""
from typing import NoReturn

from testcase.base import BaseTestCase
from testcase.base import random_string
from service.judge import judge
from service.errors import CompileError

class Case(BaseTestCase):

    """
    define sub testcase of java normal judge
    """

    java_src = '''
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println((a+b));  
    }
}
    '''

    def setUp(self) -> NoReturn:

        """
        set up the test case
        """

        print("\nRunning", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_java_ac(self) -> NoReturn:

        """
        test java ANSWER_CORRECT
        """

        judge_result = judge(
            self.java_base_config, self.java_src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 0)


    def test_java_wa(self) -> NoReturn:

        """
        test java WRONG_ANSWER
        """

        src = '''
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println((a+b+1));  
    }
}
'''
        judge_result = judge(
            self.java_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_java_tle(self) -> NoReturn:

        """
        test java cpu time limit exceeded
        """

        judge_result = judge(
            self.java_base_config, self.java_src, 1, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 1)

    def test_java_mle(self) -> NoReturn:

        """
        test java memory limit exceeded
        """

        judge_result = judge(
            self.java_base_config, self.java_src, 1000, 1, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_java_re(self) -> NoReturn:

        """
        test java runtime error
        """

        src = '''
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        String a=in.nextLine();
        String b=in.nextLine();
        System.out.println((a+b));
    }
}
'''

        judge_result = judge(
            self.java_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
        )

        for result in judge_result:
            self.assertEqual(result["result"], 4)

    def test_java_ce(self) -> NoReturn:

        """
        test java compile error
        """

        src = '''
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        String a=in.nextLine();
        int b=in.nextLine();
        System.out.println((a+b));
    }
}
'''

        try:
            judge(
                self.java_base_config, src, 1000, 128*1024*1024, random_string(), "normal",
            )
        except CompileError as exception:
            self.assertEqual(type(exception), CompileError)

    def test_java_unicode(self) -> NoReturn:

        """
        test java can run when have unicode strings
        """

        src = '''
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        String a=in.nextLine();
        System.out.println((a));
    }
}
'''

        judge_result = judge(
            self.java_base_config, src, 1000, 128*1024*1024, random_string(), "unicode",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 0)

    def test_java_other_class_name(self) -> NoReturn:

        """
        test java with other class name
        """

        src = '''
import java.util.Scanner;
public class APlusB{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println((a+b));  
    }
}
'''
        try:
            judge_result = judge(
                self.java_base_config, src, 1000, 128*1024*1024, random_string(), "normal", "APlusB"
            )
            for result in judge_result:
                self.assertEqual(result["result"], 0)
        except CompileError as exception:
            self.assertEqual(type(exception), CompileError)
