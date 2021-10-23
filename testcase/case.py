from testcase.base import BaseTestCase
from service.judge import judge
from service.judge import compile_spj
from service.errors import CompileError
from random import randint


"""
result return value
WRONG_ANSWER = -1
ANSWER_CORRECT = 0
CPU_TIME_LIMIT_EXCEEDED = 1
REAL_TIME_LIMIT_EXCEEDED = 2
MEMORY_LIMIT_EXCEEDED = 3
RUNTIME_ERROR = 4
SYSTEM_ERROR = 5
"""

class Case(BaseTestCase):
    def setUp(self):
        print("Running", self._testMethodName)
        self.workspace = self.init_workspace("case")

    def test_miss_test_case_id(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\nprint(a+b)"
        try :
            judge(
                config, src, 1000, 128, "test1"
            )
        except Exception as e:
            self.assertEqual(e, "invalid parameter")
    
    def test_ac(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\nprint(a+b)"
        judge_result = judge(
            config, src, 1000, 128*1024*1024, "test1", "normal",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 0)

    def test_wa(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\nprint(a+b+1)"
        judge_result = judge(
            config, src, 1000, 128*1024*1024, "test1", "normal",
        )
        for result in judge_result:
            self.assertEqual(result["result"], -1)

    def test_cpu_time_limit(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\nprint(a+b)"
        judge_result = judge(
            config, src, 1, 128*1024*1024, "test1", "normal",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 1)
    
    def test_memory_limit(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\nprint(a+b)"
        judge_result = judge(
            config, src, 1000, 1, "test1", "normal",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 3)

    def test_runtime(self):
        config = self.base_config
        src = "a = map(int,input().split())\nprint(a+b)"
        judge_result = judge(
            config, src, 1000, 128*1024*1024, "test1", "normal",
        )
        for result in judge_result:
            self.assertEqual(result["result"], 4)

    def test_compile_error(self):
        config = self.base_config
        src = "a, b = map(int,input().split())\n\tprint(a+b)"
        try:
            judge(
                config, src, 1000, 128*1024*1024, "test1", "normal",
            )
        except Exception as e:
            self.assertEqual(type(e), CompileError)
    
    def test_spj_compile_success(self):
        c_spj_src = "#include <stdio.h>\nint main(){\n\treturn 1;\n}"
        config = self.spj_base_config
        try:
            result = compile_spj(randint(1,1024), c_spj_src, config)
            self.assertEqual(result, "success")
        except Exception as e:
            print(e.message)
            self.assertEqual(type(e), None)
