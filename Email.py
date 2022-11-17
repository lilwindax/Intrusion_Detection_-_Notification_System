# # import packages
# # below packages are built-in - no need to install anything new!
# # yupi :)
# import smtplib
# from email.message import EmailMessage
#
# # set your email and password
# # please use App Password
# email_address = "testtargetemail121362472357@gmail.com"
# email_password = "pabumnvgcdzhipsy"
#
# # create email
# msg = EmailMessage()
# msg['Subject'] = "Email subject"
# msg['From'] = email_address
# msg['To'] = "rawinder457@gmail.com"
# msg.set_content("This is eamil message")
#
# # send email
# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#     smtp.login(email_address, email_password)
#     smtp.send_message(msg)
#
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def Send_Email(email_address, detection_image):
    fromaddr = "testtargetemail121362472357@gmail.com"
    toaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Detection Notification"

    body = "Dear user there has been a detection. Please see attachment below: "

    msg.attach(MIMEText(body, 'plain'))

    filename = detection_image
    attachment = open(detection_image, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "pabumnvgcdzhipsy")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()