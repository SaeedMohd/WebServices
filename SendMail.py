import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

def sendMailTo(userMail, tempPass):
    sender_email = "sherif@pacificresearchgroup.com"
    receiver_email = userMail
    password = "smmmo1985"

    message = MIMEMultipart("alternative")
    message["Subject"] = "ACE AAR Inspection: Reset Password"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = ""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           It was requested to reset your password for ACE AAR Inspection App Account.<br>
           This is you Temp Password: <b>{tempPass}</b>
           <br><br>
    
           If you didn't ask to reset your password, you can ignore this email.<br><br>
    
           Thanks,<br>
           ACE AAR Inspection Team
        </p>
      </body>
    </html>
    """.format(tempPass=tempPass)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def sendPDFTo(userMail, fileName, type):
    sender_email = "sherif@pacificresearchgroup.com"
    receiver_email = userMail
    password = "smmmo1985"

    message = MIMEMultipart()
    message["Subject"] = "ACE AAR Inspection: Visitation PDF for " + type
    message["From"] = sender_email
    message["To"] = userMail
    # message["CC"] = 'saeed@pacificresearchgroup.com'

    filePath = '/var/www/Inspection/WebServices/PRG/uploads/' + fileName
    attachment = MIMEBase('application', "octet-stream")
    attachment.set_payload(open(filePath, "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment; filename=' + fileName + '')


    html = """\
    <html>
      <body>
        <p>Hi,<br>
           Please find attached Visitation PDF.<br>
           <br><br>
           Thanks,<br>
           ACE AAR Inspection Team
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(attachment)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
