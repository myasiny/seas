# import code
# import sys
# from cStringIO import StringIO
#
#
# def func():
#     old_stdout = sys.stdout
#     sys.stdout = StringIO()
#     redirected_output = sys.stdout
#
#     script = 'def summ(a,b):\n\tprint a+b\nsumm(2,3)'
#     co = code.compile_command(script, "<stdin>", "exec")
#     exec(co)
#     sys.stdout = old_stdout
#
#     print  redirected_output.getvalue()
#
# script = 'def summ(a,b):\n\tprint a+b\nsumm(2,3)'
# to_compile = open("a.py","w")
# to_compile.write(script)
# to_compile.close()
# from subprocess import *
# call('python a.py')

import subprocess
from threading import Timer
kill = lambda process: process.kill()
cmd = ['python', 'a.py']
run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
my_timer = Timer(5, kill, [run])

try:
    my_timer.start()
    stdout, stderr = run.communicate()
finally:
    my_timer.cancel()



print stderr,stdout