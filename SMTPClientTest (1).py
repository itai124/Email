import smtplib
import email.utils
import socket
import imaplib
from email.mime.text import MIMEText



IPAddr = socket.gethostbyname( socket.gethostname())
print("Your Computer IP Address is: " + IPAddr)
# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient-', IPAddr))
msg['From'] = email.utils.formataddr(('Author-', '172.16.10.98'))
msg['Subject'] = 'Simple test message'


realpass="1234"
password=raw_input("enter password to connect: ")

if(realpass==password):
    # remember to change the ip of the server
    server = smtplib.SMTP('172.16.10.159', 1025)
    print "opening connection to smtp server"
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail(IPAddr, '172.16.10.159', msg.as_string())
    finally:
        print "sending email..."
        server.quit()
else:
    print "this isn't the password, you cant enter mine email server, :(("

'''
M = imaplib.IMAP4('172.16.10.159',143)
M.login(getpass.getuser(), getpass.getpass())
M.select()
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    print 'Message %s\n%s\n' % (num, data[0][1])
M.close()
M.logout()
'''

