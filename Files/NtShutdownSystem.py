import ctypes

class Shutdown:
    def __init__(self):
        self.ntdll = ctypes.WinDLL(
            'ntdll.dll',
            use_last_error=True
        )

        self.RtlAdjustPrivilege = self.ntdll.RtlAdjustPrivilege
        self.RtlAdjustPrivilege.argtypes = [
            ctypes.c_ulong,
            ctypes.c_long,
            ctypes.c_long,
            ctypes.POINTER(
                ctypes.c_long
            )
        ]
        self.RtlAdjustPrivilege.restype = ctypes.c_long

    def set_privilege(self):
        if self.RtlAdjustPrivilege(
            19, # Privilege (SE_SHUTDOWN_PRIVILEGE)
            True, # Enable Privilege
            False, # Current Thread
            ctypes.byref(
                ctypes.c_long(0)
            ) # Byref Previous Value As UInt
        ):
            return False

        else:
            return True

    def shutdown_system(self):
        if self.set_privilege():
            return self.ntdll.NtShutdownSystem(
                False # ShutdownNoReboot Action
            )

if __name__ == '__main__':
    shutdown = Shutdown()
    shutdown.shutdown_system()
