import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sentMail(auth, instructorName):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('wivernsoft', 'Dragos!2017')
    for i in auth:
        me = "Wivern Software"
        you = i[1]
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your SEAS Account"
        msg['From'] = me
        msg['To'] = you
        html = """\
<center style="width: 100%; background: #222222; text-align: left;">
<div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">Your registration has successfully completed by your instructor, please check this e-mail in order to learn your username and password information.</div>
<div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">&nbsp;</div>
<table class="email-container" style="margin: auto;" role="presentation" border="0" width="600" cellspacing="0" cellpadding="0" align="center">
<tbody>
<tr>
<td style="padding: 20px 0; text-align: center;"><a href="https://www.wivernsoftware.com/seas-en"><img style="height: auto; background: #222222; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;" src="http://pichoster.net/images/2018/03/16/ba1e2fd81ca26af117ef9357e5f21d0b.png" alt="SEAS" width="200" height="50" border="0" /></a></td>
</tr>
</tbody>
</table>
<table class="email-container" style="margin: auto;" role="presentation" border="0" width="600" cellspacing="0" cellpadding="0" align="center">
<tbody>
<tr>
<td align="center" bgcolor="#ffffff"><img class="g-img" style="width: 100%; max-width: 600px; height: auto; background: #dddddd; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; margin: auto;" src="http://pichoster.net/images/2018/03/16/cf75c98bb45b7b71bd417893e173d967.png" alt="Smart Exam Administration System" width="600" height="" align="center" border="0" /></td>
</tr>
<tr>
<td style="padding: 40px 40px 20px; text-align: center;" bgcolor="#ffffff">
<h1 style="margin: 0; font-family: sans-serif; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">Welcome to SEAS, """+i[0]+"""!</h1>
</td>
</tr>
<tr>
<td style="padding: 0 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; text-align: center;" bgcolor="#ffffff">
<p style="margin: 0;">Your account has successfully created by your instructor, """+instructorName.title()+""". <br /><br />Use the credentials stated below in order to access your account. <br /><br /><strong>Username:&nbsp;</strong>"""+i[-1]+"""<br /><strong>Password:&nbsp;</strong>"""+i[-2]+""" <br /><br />Have a good semester!<br/><br/></p>
<a href="https://www.wivernsoftware.com"><img  src="http://pichoster.net/images/2018/03/16/0d92de1a3925937304d51cf872cd646b.png" alt="Wivern Software" width="200" height="50" border="0" /></a></td>
</tr>
<tr>
<td style="padding: 0 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;" bgcolor="#ffffff">
<table style="margin: auto;" role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
<tbody>
<tr>
<td class="button-td" style="border-radius: 3px; background: #222222; text-align: center;"><a class="button-a" style="background: #222222; border: 15px solid #222222; font-family: sans-serif; font-size: 13px; line-height: 110%; text-align: center; text-decoration: none; display: block; border-radius: 3px; font-weight: bold;" href="https://www.wivernsoftware.com/"> &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ffffff;">Contact Us</span>&nbsp;&nbsp;&nbsp;&nbsp; </a></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</center>
"""

        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        mail.sendmail(me, you, msg.as_string())

        print 'Email sent for %s!' % i[0]

    mail.quit()

# auth = [["Muhammed Yasin Yildirim","muhammedyildirim@std.sehir.edu.tr","msj123SaL","muhammedyildirim"]]
# instructorName = "Ali Cakmak"
# sentMail(auth, instructorName)