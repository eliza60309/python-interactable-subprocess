import fdhandler
import subprocess

class subprocesswithfd():
    '''
    usage:
        process = subprocesswithfd.subprocesswithfd(['a.exe'], stderr=True, stdout=True, stdin=True)
        process.stdin.write("hi")
        string = process.stdout.read()
        string = process.stderr.read()
    '''
    def __init__(self, args, stdin=False, stdout=False, stderr=False):
        _stdin = subprocess.PIPE if stdin else None
        _stdout = subprocess.PIPE if stdout else None
        _stderr = subprocess.PIPE if stderr else None
        process = subprocess.Popen(args, stdin=_stdin, stdout=_stdout, stderr=_stderr)
        if stdin:
            self.stdin = fdhandler.writer(process.stdin)
        if stdout:
            self.stdout = fdhandler.reader(process.stdout)
            self.stdout.start()
        if stderr:
            self.stderr = fdhandler.reader(process.stderr)
            self.stderr.start()

        
if __name__ == "__main__":
    pass
    




