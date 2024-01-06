# coding=utf-8
from __future__ import print_function, absolute_import
from datetime import datetime
import random
import os
from gm.api import *

_gm_libs_logs = {
    "common": "",
}


# 日志输出且保存
def log_all(level: str, info: str, source: str = "", filetype: str = "common"):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    print(text)
    append(text, filetype)


# 日志不输出仅保存
def log_save(level: str, info: str, source: str = "", filetype: str = "common"):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    append(text, filetype)


# 追加信息到日志文件
def append(text: str, filetype: str = ""):
    global _gm_libs_logs
    parent_path = r"C:\Users\Public\gm_libs"

    if filetype not in _gm_libs_logs or _gm_libs_logs[filetype] == "":
        _gm_libs_logs[filetype] = ""
        hash_name = random.getrandbits(64)

        _gm_libs_logs[filetype] = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "%032x" % hash_name
        all_path = r"{}\{}".format(parent_path, _gm_libs_logs[filetype])

        if not os.path.exists(parent_path):
            os.mkdir(parent_path)
        os.mkdir(all_path)
        log_file = open(r"{}\{}.log".format(all_path, filetype), "w+", encoding="utf-8")
    else:
        all_path = r"{}\{}".format(parent_path, _gm_libs_logs[filetype])
        log_file = open(r"{}\{}.log".format(all_path, filetype), "a", encoding="utf-8")

    log_file.writelines("{}\n".format(text))
    log_file.close()
