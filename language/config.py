"""
Language configuration file.
"""
import copy


class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


class LanguageConfig():
    """
    Language config
    """

    default_env = ["LANG=en_US.UTF-8",
                   "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"]
    _java_lang_config = {
        "compile": {
            "src_name": "{program_name}.java",
            "exe_name": "{program_name}.class",
            "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8"
        },
        "run": {
            "command": "/usr/bin/java -cp {exe_dir} -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 "
            "-Djava.security.policy==/etc/java_policy -Djava.awt.headless=true {program_name}",
            "seccomp_rule": None,
            "env": default_env,
            "memory_limit_check_only": 1
        }
    }
    _c_lang_config = {
        "compile": {
            "src_name": "{program_name}.c",
            "exe_name": "{program_name}",
            "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c11 {src_path} -lm -o {exe_path}",
        },
        "run": {
            "command": "{exe_path}",
            "seccomp_rule": {ProblemIOMode.standard: "c_cpp", ProblemIOMode.file: "c_cpp_file_io"},
            "env": default_env
        }
    }
    _cpp_lang_config = {
        "compile": {
            "src_name": "{program_name}.cpp",
            "exe_name": "{program_name}",
            "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++14 {src_path} -lm -o {exe_path}",
        },
        "run": {
            "command": "{exe_path}",
            "seccomp_rule": {ProblemIOMode.standard: "c_cpp", ProblemIOMode.file: "c_cpp_file_io"},
            "env": default_env
        }
    }

    _py3_lang_config = {
        "compile": {
            "src_name": "{program_name}.py",
            "exe_name": "__pycache__/{program_name}.cpython-36.pyc",
            "compile_command": "/usr/bin/python3 -m py_compile {src_path}",
        },
        "run": {
            "command": "/usr/bin/python3 {exe_path}",
            "seccomp_rule": "general",
            "env": default_env + ["PYTHONIOENCODING=utf-8"]
        }
    }

    def __init__(self, language, cpu, memory):
        switch = {
            "python3": self.py3_base_config,
            "clang": self.c_base_config,
            "cpp": self.cpp_base_config,
            "java": self.java_base_config
        }

        self.config = switch.get(language, None)
        if self.config is None:
            return

        self.config["compile"]["max_cpu_time"] = cpu
        self.config["compile"]["max_real_time"] = cpu
        self.config["compile"]["max_memory"] = memory

    @property
    def py3_base_config(self):
        """return python3 base configuration"""
        return copy.deepcopy(self._py3_lang_config)

    @property
    def java_base_config(self):
        """return java base configuration"""
        return copy.deepcopy(self._java_lang_config)

    @property
    def c_base_config(self):
        """return c base configuration"""
        return copy.deepcopy(self._c_lang_config)

    @property
    def cpp_base_config(self):
        """return cpp base configuration"""
        return copy.deepcopy(self._cpp_lang_config)

    @property
    def default(self):
        """return default configuration"""
        return None
