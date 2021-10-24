"""
define all function related to judge submission
"""

import os
import shutil
from typing import Union
from typing import NoReturn

from .compiler import Compiler
from .utils import logger
from .errors import JudgeClientError
from .errors import CompileError
from .errors import SPJCompileError
from .config import ProblemIOMode
from .config import SPJ_EXE_DIR
from .config import COMPILER_USER_UID
from .config import RUN_GROUP_GID
from .config import JUDGER_WORKSPACE_BASE
from .config import TEST_CASE_DIR
from .config import RUN_USER_UID
from .config import SPJ_SRC_DIR
from .config import SPJ_USER_UID
from .judge_client import JudgeClient


DEBUG = os.environ.get("judger_debug") == "1"


class InitSubmissionEnv(object):
    """
    create environment for submission and delete when done
    """
    def __init__(self, judger_workspace: str, submission_id: str):
        self.work_dir = os.path.join(judger_workspace, submission_id)

    def __enter__(self) -> str:
        try:
            os.mkdir(self.work_dir)
            os.chown(self.work_dir, COMPILER_USER_UID, RUN_GROUP_GID)
            os.chmod(self.work_dir, 0o710)
        except OSError as exception:
            logger.exception(exception)
            JudgeClientError("failed to create runtime dir")
        return self.work_dir

    def __exit__(self, exc_type, exc_val, exc_tb)  -> NoReturn:
        if not DEBUG:
            try:
                shutil.rmtree(self.work_dir)
            except OSError as exception:
                logger.exception(exception)
                JudgeClientError("failed to clean runtime dir")


def judge(  language_config: dict, src: str, max_cpu_time: int, max_memory: int,
            submission_id: str, test_case_id: str = None,
            program_name: str = None, output: bool = False,
            spj_version: str = None, spj_config: dict = None,
            spj_compile_config: dict = None, spj_src: str = None) -> Union[list, None]:

    """
    judge submission
    """

    if not test_case_id:
        JudgeClientError("invalid parameter")
        return

    if program_name is None:
        program_name = "Main"

    compile_config = language_config.get("compile")
    compile_config["src_name"] = compile_config["src_name"].format(program_name=program_name)
    compile_config["exe_name"] = compile_config["exe_name"].format(program_name=program_name)
    run_config = language_config["run"]
    io_mode = {"io_mode": ProblemIOMode.standard}
    is_spj = spj_version and spj_config

    if is_spj:
        exe_name = spj_config["exe_name"].format(spj_version=spj_version)
        spj_exe_path = os.path.join(SPJ_EXE_DIR, exe_name)
        # spj src has not been compiled
        if not os.path.isfile(spj_exe_path):
            logger.warning("%s does not exists, spj src will be recompiled")
            compile_spj(spj_version=spj_version, src=spj_src,
                        spj_compile_config=spj_compile_config)

    with InitSubmissionEnv(JUDGER_WORKSPACE_BASE, submission_id=str(submission_id)) as tmp_dir:
        submission_dir = tmp_dir
        test_case_dir = os.path.join(TEST_CASE_DIR, test_case_id)

        if compile_config:
            src_path = os.path.join(submission_dir, compile_config["src_name"])

            # write source code into file
            with open(src_path, "w", encoding="utf-8") as file:
                file.write(src)
            os.chown(src_path, COMPILER_USER_UID, 0)
            os.chmod(src_path, 0o400)
            # compile source code, return exe file path
            exe_path = Compiler().compile(
                compile_config=compile_config,
                src_path=src_path,
                output_dir=submission_dir
            )
            try:
                # Java exe_path is SOME_PATH/Main, but the real path is SOME_PATH/Main.class
                # We ignore it temporarily
                os.chown(exe_path, RUN_USER_UID, 0)
                os.chmod(exe_path, 0o500)
            except OSError as exception:
                print("Exception %s", exception)
        else:
            exe_path = os.path.join(submission_dir, run_config["exe_name"])
            with open(exe_path, "w", encoding="utf-8") as file:
                file.write(src)

        judge_client = JudgeClient(run_config=language_config["run"],
                                       exe_path=exe_path,
                                       program_name=program_name,
                                       max_cpu_time=max_cpu_time,
                                       max_memory=max_memory,
                                       test_case_dir=test_case_dir,
                                       submission_dir=submission_dir,
                                       spj_version=spj_version,
                                       spj_config=spj_config,
                                       output=output,
                                       io_mode=io_mode)
        run_result = judge_client.run()
        return run_result


def compile_spj(spj_version: str, src: str, spj_compile_config: dict):

    """
    function of compile special judge
    """

    spj_compile_config["src_name"] = spj_compile_config["src_name"].format(spj_version=spj_version)
    spj_compile_config["exe_name"] = spj_compile_config["exe_name"].format(spj_version=spj_version)

    spj_src_path = os.path.join(SPJ_SRC_DIR, spj_compile_config["src_name"])

    # if spj source code not found, then write it into file
    if not os.path.exists(spj_src_path):
        with open(spj_src_path, "w", encoding="utf-8") as file:
            file.write(src)
        os.chown(spj_src_path, COMPILER_USER_UID, 0)
        os.chmod(spj_src_path, 0o400)
    try:
        exe_path = Compiler().compile(
            compile_config=spj_compile_config, src_path=spj_src_path, output_dir=SPJ_EXE_DIR
        )
        os.chown(exe_path, SPJ_USER_UID, 0)
        os.chmod(exe_path, 0o500)
    # turn common CompileError into SPJCompileError
    except CompileError as excpetion:
        raise SPJCompileError(excpetion.message) from excpetion
    return "success"
