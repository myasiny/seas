import os
import subprocess32 as subprocess
import sys

def run_script_without_func(python_path,file_path,file_name):
    file = file_path+"\\"+file_name
    # a = os.popen('%s %s' %(python_path,file)).read()
    a = subprocess.check_output(('%s %s' % (python_path, file)), stderr=subprocess.STDOUT, timeout=10)
    return a

def run_script_with_func(python_path,file_path,file_name_without_extension,function_name,inputs):
    inputs_str = ""
    for i in inputs:
        inputs_str = inputs_str + "'" +str(i) + "'" +","
    inputs_str = inputs_str[0:-1]
    os.chdir("%s" %file_path)
    print """%s -c "from %s import *; print %s(%s)" """ %(python_path,file_name_without_extension,function_name,inputs_str)
    a = os.popen("""%s -c "from %s import *; print %s(%s)" """ %(python_path,file_name_without_extension,function_name,inputs_str)).read()
    return a


# # Question without function, just output
# PYTHON_PATH = sys.executable
# file_path = "C:\Users\\aliem\Desktop\Q"
# file_name = "Q3.py"
# file_name_without_extension = "Q3"
# answer = run_script_without_func(python_path=PYTHON_PATH, file_path=file_path, file_name=file_name)
# print answer


"""
# Question with function, without input
PYTHON_PATH = sys.executable
file_path = "C:\Users\\aliem\Desktop\Q"
file_name = "Q2.py"
file_name_without_extension = "Q2"
function_name = ""
answer = run_script_with_func(python_path=PYTHON_PATH, file_path=file_path, file_name_without_extension=file_name_without_extension, function_name="sayHello",inputs = [] )
print answer


true_answer = (open("C:\Users\\aliem\Desktop\Q\\A2.txt","r").read()) + "\n"
if answer == true_answer:
    print True
else:
    print False
"""

"""
# Question with function, with input
PYTHON_PATH = sys.executable
file_path = "C:\Users\\aliem\Desktop\Q"
file_name = "Q1.py"
file_name_without_extension = "Q1"
function_name = "greet"

inputt = ["Ali Emre","Oz"]


answer = run_script_with_func(python_path=PYTHON_PATH, file_path=file_path, file_name_without_extension=file_name_without_extension, function_name=function_name, inputs = inputt )
print answer


true_answer = (open("C:\Users\\aliem\Desktop\Q\\A1.txt","r").read()) + "\n"
print answer
"""