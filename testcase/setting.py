class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


default_env = ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"]

_c_lang_config = {
    "compile": {
        "src_name": "{program_name}.c",
        "exe_name": "{program_name}",
        "max_cpu_time": 3000,
        "max_real_time": 10000,
        "max_memory": 256 * 1024 * 1024,
        "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c11 {src_path} -lm -o {exe_path}",
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": {ProblemIOMode.standard: "c_cpp", ProblemIOMode.file: "c_cpp_file_io"},
        "env": default_env
    }
}

_c_lang_spj_compile = {
    "src_name": "spj-{spj_version}.c",
    "exe_name": "spj-{spj_version}",
    "max_cpu_time": 3000,
    "max_real_time": 10000,
    "max_memory": 1024 * 1024 * 1024,
    "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c11 {src_path} -lm -o {exe_path}"
}

_c_lang_spj_config = {
    "exe_name": "spj-{spj_version}",
    "command": "{exe_path} {in_file_path} {user_out_file_path}",
    "seccomp_rule": "c_cpp"
}

_cpp_lang_config = {
    "compile": {
        "src_name": "{program_name}.cpp",
        "exe_name": "{program_name}",
        "max_cpu_time": 10000,
        "max_real_time": 20000,
        "max_memory": 1024 * 1024 * 1024,
        "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++14 {src_path} -lm -o {exe_path}",
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": {ProblemIOMode.standard: "c_cpp", ProblemIOMode.file: "c_cpp_file_io"},
        "env": default_env
    }
}

_cpp_lang_spj_compile = {
    "src_name": "spj-{spj_version}.cpp",
    "exe_name": "spj-{spj_version}",
    "max_cpu_time": 10000,
    "max_real_time": 20000,
    "max_memory": 1024 * 1024 * 1024,
    "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++14 {src_path} -lm -o {exe_path}"
}

_cpp_lang_spj_config = {
    "exe_name": "spj-{spj_version}",
    "command": "{exe_path} {in_file_path} {user_out_file_path}",
    "seccomp_rule": "c_cpp"
}

_java_lang_config = {
    "compile": {
        "src_name": "{program_name}.java",
        "exe_name": "{program_name}",
        "max_cpu_time": 5000,
        "max_real_time": 10000,
        "max_memory": -1,
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

_py3_lang_config = {
    "compile": {
        "src_name": "{program_name}.py",
        "exe_name": "__pycache__/{program_name}.cpython-36.pyc",
        "max_cpu_time": 3000,
        "max_real_time": 10000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/python3 -m py_compile {src_path}",
    },
    "run": {
        "command": "/usr/bin/python3 {exe_path}",
        "seccomp_rule": "general",
        "env": default_env + ["PYTHONIOENCODING=utf-8"]
    }
}

_go_lang_config = {
    "compile": {
        "src_name": "{program_name}.go",
        "exe_name": "{program_name}",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 1024 * 1024 * 1024,
        "compile_command": "/usr/bin/go build -o {exe_path} {src_path}",
        "env": ["GOCACHE=/tmp", "GOPATH=/tmp", "GOMAXPROCS=1"] + default_env
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": "golang",
        # 降低内存占用
        "env": ["GODEBUG=madvdontneed=1", "GOMAXPROCS=1"] + default_env,
        "memory_limit_check_only": 1
    }
}

languages = [
    {"config": _c_lang_config, "spj": {"compile": _c_lang_spj_compile, "config": _c_lang_spj_config},
     "name": "C", "description": "GCC 9.4", "content_type": "text/x-csrc"},
    {"config": _cpp_lang_config, "spj": {"compile": _cpp_lang_spj_compile, "config": _cpp_lang_spj_config},
     "name": "C++", "description": "G++ 9.4", "content_type": "text/x-c++src"},
    {"config": _java_lang_config, "name": "Java",
        "description": "OpenJDK 11", "content_type": "text/x-java"},
    {"config": _py3_lang_config, "name": "Python3",
        "description": "Python 3.6", "content_type": "text/x-python"},
    {"config": _go_lang_config, "name": "Golang",
        "description": "Golang 1.17", "content_type": "text/x-go"},
]
