import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket

# main
SMTP_PORT = 2025
IMAP_PORT = 143
counter=0
IPAddr = socket.gethostbyname(socket.gethostname())
thread = threading.Thread(
    target=localmail.run,
    args=(SMTP_PORT, IMAP_PORT, 8880, 'localmail.mbox')
)
thread.start()
print "waiting for clients"




#localmail.shutdown_thread(thread)
#print "shutdown localmail"