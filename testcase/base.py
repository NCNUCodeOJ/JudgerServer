import os
import shutil
from unittest import TestCase



class BaseTestCase(TestCase):
    BAD_SYSTEM_CALL = 31
    default_env = ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"]

    def init_workspace(self, language):
        base_workspace = "/tmp"
        workspace = os.path.join(base_workspace, language)
        shutil.rmtree(workspace, ignore_errors=True)
        os.makedirs(workspace)
        return workspace



    @property
    def base_config(self):
        config = {
            "compile": {
                "src_name": "solution.py",
                "exe_name": "__pycache__/solution.cpython-36.pyc",
                "max_cpu_time": 3000,
                "max_real_time": 10000,
                "max_memory": 128 * 1024 * 1024,
                "compile_command": "/usr/bin/python3 -m py_compile {src_path}",
            },
            "run": {
                "command": "/usr/bin/python3 {exe_path}",
                "seccomp_rule": "general",
                "env": self.default_env + ["PYTHONIOENCODING=utf-8"]
            }
        }
        return config
    
    @property
    def spj_base_config(self):
        config = {
            "src_name": "spj-{spj_version}.c",
            "exe_name": "spj-{spj_version}",
            "max_cpu_time": 3000,
            "max_real_time": 5000,
            "max_memory": 1024 * 1024 * 1024,
            "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 {src_path} -lm -o {exe_path}"
        }
        return config