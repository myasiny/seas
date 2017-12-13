from requests import put, get, post, delete
from DatabaseAPI import *

### Sample usage of API


# print addOrganization("http://10.50.81.24:8888", "Istanbul Sehir University")
# print addOrganization("http://10.50.81.24:8888", "Istanbul Technical University")
# #
# print addUser("http://10.50.81.24:8888", "Istanbul Technical University", "213962062", "Sahin", "Dogan", "sahindogan", "12345",role="student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "213955555", "Muhammed Yasin", "Yildirim", "muhammedyildirim", "12345", role="student")
#
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "213944444", "Ali Emre", "Oz", "alioz", "12345", role="student")
# print addUser("http://10.50.81.24:8888", "Istanbul Sehir University", "000000000", "Admin", "Admin", "admin", "12345", role="Admin")

print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "alioz", "1234")
print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "aliozz", "12345")
print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "alioz", "12345")
# print signIn("http://10.50.81.24:8888", "Istanbul Sehir University", "admin", "12345")

