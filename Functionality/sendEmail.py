import smtplib
from passwordGenerator import passwordGenerator

def sentMail(gmail_user,gmail_pass,to,studentName,instructorName):

    subject = 'About your SEAS Account'

    content = "Hi, %s \n\n\n" \
              "Welcome to SEAS. \n\n\n" \
              "Your account was created by your instructor %s.\n\n\n" \
              "Your password is : %s \n\n\n" \
              "You can change it from SEAS Login page\n\n\n" \
              "You can access your account by your student ID or your email.\n\n\n" \
              "Wivern Software, 2018" % (studentName, instructorName, passwordGenerator(8))
    sent_from = "SEAS by Wivern Software"
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sent_from, to, subject, content)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(gmail_user, gmail_pass)
    server.sendmail(sent_from, to, message)
    server.close()

    print 'Email sent for %s!' %studentName

gmail_user = 'alioz@std.sehir.edu.tr'
gmail_pass = "YOUR PASSWORD"
instructorName = "Ali Cakmak"
people_dict = {"Ali Emre Oz":"alioz@std.sehir.edu.tr","Ali Emre Oz 2":"aliemreoz@outlook.com"}

for i in people_dict:
    sentMail(gmail_user,gmail_pass,people_dict[i],i,instructorName)