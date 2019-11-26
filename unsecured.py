import pprint
import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket
from email.mime.text import MIMEText

def smtp_mail():
    msg = MIMEText('This is the body of the message.')
    msg['To'] = email.utils.formataddr(('Recipient-', IPAddr))
    msg['From'] = email.utils.formataddr(('Author-', '172.16.10.98'))
    msg['Subject'] = 'Simple test message'

    server = smtplib.SMTP(IPAddr, SMTP_PORT)
    server.login('user', 'password')
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail(IPAddr, '172.16.10.98', msg.as_string())
        print "sending email..."
    except:
        print  "no"
    finally:
        server.quit()
    
def fetch_mail_msg():
    imap = imaplib.IMAP4(IPAddr,IMAP_PORT)
    imap.login('username', 'password')
    imap.select('Inbox')
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
            tmp, data = imap.fetch(num, '(RFC822)')
            print('Message: {0}\n'.format(num))
            pprint.pprint(data[0][1])
            break
    imap.close()

# main
SMTP_PORT = 2025
IMAP_PORT = 143
IPAddr = socket.gethostbyname( socket.gethostname())
thread = threading.Thread(
   target=localmail.run,
   args=(SMTP_PORT, IMAP_PORT, 8880, 'localmail.mbox') 
)
thread.start()

smtp_mail()
fetch_mail_msg()
    
localmail.shutdown_thread(thread)
print "shutdown localmail"
