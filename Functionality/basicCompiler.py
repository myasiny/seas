import code
import sys
from cStringIO import StringIO
import math
old_stdout = sys.stdout
sys.stdout = StringIO()
redirected_output = sys.stdout

script = 'def summ(a,b):\n\tprint a+b\nsumm(2,3)'
co = code.compile_command(script, "<stdin>", "exec")
exec(co)
sys.stdout = old_stdout

print redirected_output.getvalue()