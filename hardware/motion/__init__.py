import platform

system = platform.system()

match system:
    case "Windows":
        from ._thorlabs import *
    case "Darwin":
        pass
