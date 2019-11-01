import fdhandler

class subprocesswfd():
    '''
    usage:
        process = subprocesswfd(['a.exe'], stderr=True, stdout=True, stdin=True)
        process.stdin.write("hi")
        ss = process.stdout.read()
        print(ss)
    '''