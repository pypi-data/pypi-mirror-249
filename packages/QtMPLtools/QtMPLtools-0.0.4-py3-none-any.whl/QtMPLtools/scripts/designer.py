def main():
    import subprocess as sp
    import os, sys

    if os.name == 'posix':
        exp = 'export PYQTDESIGNERPATH=' + os.path.dirname(os.path.realpath(sys.argv[0]))
    elif os.name == 'nt':
        exp = 'setx PYQTDESIGNERPATH ' + os.path.dirname(os.path.realpath(sys.argv[0]))

    sp.Popen(exp, shell=True).wait()
    sp.Popen("pyqt6-tools designer", shell=True, stdout=sp.DEVNULL)
