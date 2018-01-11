import smtplib

def sentMail(auth,instructorName):
    gmail_user = "wivernsoft@gmail.com"
    gmail_pass = "Dragos!2017"
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(gmail_user, gmail_pass)

    for i in auth:
        subject = 'About your SEAS Account'

        content = "Hi, %s \n\n\n" \
                  "Welcome to SEAS. \n\n\n" \
                  "Your account was created by your instructor %s.\n\n\n" \
                  "Your password is : %s \n\n\n" \
                  "You can change it from SEAS Login page\n\n\n" \
                  "You can access your account by your student ID or your email.\n\n\n" \
                  "Wivern Software, 2018" % (i[0], instructorName, i[2])
        sent_from = "SEAS by Wivern Software"
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (sent_from, i[1], subject, content)
        server.sendmail(sent_from, i[1], message)
        print 'Email sent for %s!' %i[0]
    server.close()