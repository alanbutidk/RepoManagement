import time
import sys
import os

class ArgumentNotGivenError(Exception):
    pass
class Task:
    SuccessFileExistsCode = 0
    OSErrorCode = 0
    def wait(n):
        time.sleep(n)
    @staticmethod
    def FileExists(filename):
        try:
            if os.path.exists(filename):
                Task.SuccessFileExistsCode = 1
                print("File Exists")
            elif not os.path.exists(filename):
                Task.SuccessFileExistsCode = 0
        except OSError:
            Task.OSErrorCode = 1
            print("OSERROR")
            pass
    @staticmethod
    def ReadFromFile(filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            print("File not found")
            return "" 
            f.read()
        except FileNotFoundError:
            print("FileNotFoundError Detected, breaking")
            pass
    @staticmethod
    def WriteToFile(filename, **kwargs):
        try:
            with open(filename, "a") as f:
                if kwargs:
                    data = next(iter(kwargs.values()))
                    f.write(str(data) + "\n")
        except OSError:
            print("OSERROR")
            Task.OSErrorCode = 1
    def OverWriteToFile(filename, **kwargs):
        try:
            with open(filename, "a") as f:
                if kwargs:
                    data = next(iter(kwargs.values()))
                    f.write(str(data) + "\n")
        except OSError:
            print("OSERROR")
            sys.exit(1)
    def CheckArg(string, tell=False):
        try:
            if sys.argv:
                if tell:
                    print("\nTell is checked on")
                    print("\nArguments are:")
                    for i, arg in enumerate(sys.argv[1:]):
                        if not arg == string:
                            print("\nArgument doesnt match")
                            break
                        print(f"\nArg {i}: {arg}")
                elif string:
                    if string in sys.argv[1:]:
                        print(f"\nArgument has string given {string}")
                    elif not string in sys.argv[1:]:
                        print(f"\nArgument doesnt have string {string} given as a argument")
                elif not string:
                    sys.exit(1)
        except OSError:
            pass
    def ExitWithoutDynamicErrors(str, verbose=False):
        try:
            if verbose == True:
                print("\nExitWithoutDynamicErrors.verbose is turned on.")
                print("\nStarting Exit Process via SystemExit")
                raise SystemExit(str)
            else:
                pass
            raise SystemExit(str)
        except SystemError:
            print("SystemError was recorded, indicating Python is bugging, immediate EXIT is called!")
            sys.exit(1)


