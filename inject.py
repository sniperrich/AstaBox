# -*- coding: utf-8 -*-
from ctypes import *
import psutil
import win32api


def injectDll(string=None):
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    dll_path = "C://Users//rich//Downloads//gamesense-ltd-main//gamesense-ltd-main//build//gs.dll".encode('ascii', 'ignore')

    dll_len = len(dll_path)
    print(dll_len)
    kernel32 = windll.kernel32

    # 第一步获取整个系统的进程快照
    pids = psutil.pids()
    # 第二步在快照中去比对进程名
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == string:
            pass