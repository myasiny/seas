import smtplib

def sentMail(auth,instructorName):
    gmail_user = "wivernsoft@gmail.com"
    gmail_pass = "Dragos!2017"
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(gmail_user, gmail_pass)

    for i in auth:
        subject = 'Your SEAS Account'
        content = "Hi, %s \n\n\n" \
                  "Welcome to SEAS! \n\n\n" \
                  "Your account was created by your instructor, %s.\n\n\n" \
                  "Username: %s\n\n\n" \
                  "Password: %s \n\n\n" \
                  "Remember that, you can change or reset your password through SEAS login page whenever you need.\n\n\n" \
                  "In order to access your account on SEAS, all you need is to use the username and password provided above.\n\n\n" \
                  "Have a good day! :)\n\n\n" \
                  "Wivern Software, 2018" % (i[0], instructorName, i[3], i[2])
        sent_from = "Smart Exam Administration System"
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (sent_from, i[1], subject, content)
        server.sendmail(sent_from, i[1], message)
        print 'Email sent for %s!' % i[0]

    server.close()