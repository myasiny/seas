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
# call('python a.py', timeout=5.0)
import sys
import subprocess32 as subprocess
try:
    try:
        a = subprocess.check_output("python a.py", stderr=subprocess.STDOUT, timeout=5)

    except subprocess.CalledProcessError as e:
        a = e.output.split("\n")[-3] + "\n" + e.output.split("\n")[-2]
except:
    a = "Timeout Error"

print a