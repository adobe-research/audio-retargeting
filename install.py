#!/usr/bin/env python

import os
import re
import subprocess
import shutil
import sys

EXT_LIBS = ["libsndfile", "libsamplerate"]
PIPS = ["cython", "numpy", "scipy", "matplotlib", "scikits.audiolab", "scikits.samplerate", "librosa"]

CWD = os.getcwd()
LOGFILE = "install.log"

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def install(obj, cmd):
    def log(output):
        with open(os.path.join(CWD, LOGFILE), "a") as f:
            f.write("\n********** Installing {obj}: {cmd}\n".format(obj=obj, cmd=' '.join(cmd)))
            f.write(output)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        log(output)
    except subprocess.CalledProcessError, e:
        log(e.output)
        sys.exit("Error installing {obj}.  See log in '{logfile}'".format(obj=obj, logfile=LOGFILE))

def pip_status(mod):
    output = subprocess.check_output(["pip", "show", mod], stderr=subprocess.STDOUT)
    m = re.search('Version:\s*(\S+)', output, re.MULTILINE)
    return None if m is None else m.group(1)

def lib_status(lib):
    try:
        subprocess.check_output(["ld", "-r", "-l"+re.sub('^lib', '', lib), "-o", "/dev/null"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def main():

    if os.path.isfile(LOGFILE): shutil.move(LOGFILE, LOGFILE+".bak")

    print("*** External libraries ***")
    for i, lib in enumerate(EXT_LIBS):
        count = "[{i} of {n}]".format(i=i+1, n=len(EXT_LIBS))
        if lib_status(lib):
            print("{lib} OK {count}".format(lib=lib, count=count))
        else:
            print("-- installing {lib} {count}".format(lib=lib, count=count))
            install(lib, ["brew", "install", lib])


    print("\n*** Python modules ***")
    for i, mod in enumerate(PIPS):
        count = "[{i} of {n}]".format(i=i+1, n=len(PIPS))
        version = pip_status(mod)
        if version is None:
            print("-- installing {mod}...".format(mod=mod))
            install(mod, ["pip", "install", mod])
            version = pip_status(mod)
        print("{mod} v{version} {count}".format(mod=mod, version=version, count=count))

    print("\n*** radiotool ****")
    mod = 'radiotool'
    version = pip_status(mod)
    if version is None:
        print("installing {mod}...".format(mod=mod))
        with cd("radiotool"):
            install("radiotool", ["python", "setup.py", "install"])
        version = pip_status(mod)
    print("{mod} v{version}".format(mod=mod, version=version))

    print("\n*** retarget.py ***")
    install("retarget.py", ["python", "setup.py", "install"])
    which = subprocess.check_output(["which", "retarget.py"])
    print("Installed {retarget}".format(retarget=which))

main()
