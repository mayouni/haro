"""Runs a command under a Windows job that limits each process's committed memory, and answers its exit code.
Usage: python under_limit.py <megabytes> <command...>. The job is put on this helper itself, so the child inherits it; the
helper's own stdout and stderr are the child's. Prints nothing of its own except, on stderr, `under_limit: exit N`."""
import ctypes
import subprocess
import sys
from ctypes import wintypes

mb = int(sys.argv[1])
cmd = sys.argv[2:]
k = ctypes.WinDLL('kernel32', use_last_error=True)


class BASIC(ctypes.Structure):
    _fields_ = [('PerProcessUserTimeLimit', ctypes.c_longlong), ('PerJobUserTimeLimit', ctypes.c_longlong),
                ('LimitFlags', wintypes.DWORD), ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t), ('PriorityClass', wintypes.DWORD), ('SchedulingClass', wintypes.DWORD)]


class IOC(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in ('ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
                                                  'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]


class EXT(ctypes.Structure):
    _fields_ = [('BasicLimitInformation', BASIC), ('IoInfo', IOC), ('ProcessMemoryLimit', ctypes.c_size_t),
                ('JobMemoryLimit', ctypes.c_size_t), ('PeakProcessMemoryUsed', ctypes.c_size_t),
                ('PeakJobMemoryUsed', ctypes.c_size_t)]


k.CreateJobObjectW.restype = wintypes.HANDLE
k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
k.GetCurrentProcess.restype = wintypes.HANDLE
job = k.CreateJobObjectW(None, None)
info = EXT()
info.BasicLimitInformation.LimitFlags = 0x100  # JOB_OBJECT_LIMIT_PROCESS_MEMORY
info.ProcessMemoryLimit = mb * 1024 * 1024
if not k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):
    sys.exit('under_limit: SetInformationJobObject failed %d' % ctypes.get_last_error())
if not k.AssignProcessToJobObject(job, k.GetCurrentProcess()):
    sys.exit('under_limit: AssignProcessToJobObject failed %d' % ctypes.get_last_error())
r = subprocess.run(cmd)
sys.stderr.write('under_limit: exit %d\n' % r.returncode)
sys.exit(r.returncode & 0xFF if r.returncode >= 0 else 1)
