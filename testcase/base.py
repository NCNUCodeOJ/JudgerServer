import os
import shutil
from unittest import TestCase
from .setting import _py3_lang_config
from .setting import _c_lang_spj_compile
from .setting import _c_lang_spj_config



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
        return _py3_lang_config.copy()
    
    @property
    def spj_compile_base_config(self):
        return _c_lang_spj_compile.copy()
    
    @property
    def spj_base_config(self):
        return _c_lang_spj_config.copy()