"""
compiler class
"""
import json
import os
import shlex

# pylint: disable=import-error
import _judger
# pylint: enable=import-error

from .config import COMPILER_LOG_PATH
from .config import COMPILER_USER_UID
from .config import COMPILER_GROUP_GID
from .errors import CompileError

class Compiler(object):
    """
    Compiler class
    """
    def compile(self, compile_config, src_path, output_dir):
        """
        compile code from submission or spj
        """
        command = compile_config["compile_command"]
        exe_path = os.path.join(output_dir, compile_config["exe_name"])
        command = command.format(src_path=src_path, exe_dir=output_dir, exe_path=exe_path)
        compiler_out = os.path.join(output_dir, "compiler.out")
        _command = shlex.split(command)
        os.chdir(output_dir)
        env = compile_config.get("env", [])
        env.append("PATH=" + os.getenv("PATH"))
        result = _judger.run(max_cpu_time=compile_config["max_cpu_time"],
                             max_real_time=compile_config["max_real_time"],
                             max_memory=compile_config["max_memory"],
                             max_stack=128 * 1024 * 1024,
                             max_output_size=20 * 1024 * 1024,
                             max_process_number=_judger.UNLIMITED,
                             exe_path=_command[0],
                    # /dev/null is best, but in some system, this will call ioctl system call
                             input_path=src_path,
                             output_path=compiler_out,
                             error_path=compiler_out,
                             args=_command[1::],
                             env=env,
                             log_path=COMPILER_LOG_PATH,
                             seccomp_rule_name=None,
                             uid=COMPILER_USER_UID,
                             gid=COMPILER_GROUP_GID)
        if result["result"] != _judger.RESULT_SUCCESS:
            if os.path.exists(compiler_out):
                with open(compiler_out, encoding="utf-8") as file:
                    error = file.read().strip()
                    os.remove(compiler_out)
                    if error:
                        raise CompileError(error)
            error_msg = "Compiler runtime error, info: {result}"
            raise CompileError(error_msg.format(result=json.dumps(result)))
        os.remove(compiler_out)
        return exe_path
