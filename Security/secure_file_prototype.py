from werkzeug.utils import secure_filename

open_bi = open # overwrite built in open function

def open(a, mode):
    # Secure file name here
    a =  secure_filename(a)
    return open_bi(a, mode)

# standart open call, overwritten by us.
with open("C://asdasd.txt", "w") as f:
    print f.write("**")

with open("asdasd.txt", "w") as f:
    print f.write("***")

with open("External_Functions/asdasd.txt", "w") as f:
    print f.write("****")

