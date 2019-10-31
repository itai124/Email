import redis
import asyncore
import socket
import getpass
import  imaplib
from smtpd import SMTPServer
import smtplib

iplists=['10.100.102.6','10.100.102.7','10.100.102.8']
#getting the computer ip
IPAddr = socket.gethostbyname( socket.gethostname())
print("Your Computer IP Address is: " + IPAddr)

class CustomSMTPServer(SMTPServer):
  def process_message(self, peer, mailfrom, rcpttos, data):
    print('Receiving message from:', peer)
    print('Message addressed from:', mailfrom)
    print('Message addressed to:', rcpttos)
    print('Message length:', len(data))
    print "----------------------"
    data_body = "\n\n".join(data.split('\n\n')[1:])
    print data_body
    '''
    global iplists,rs
    for i in range(0,2):
        if(iplists[i]==peer[0]):
            #saving all the  messages
            rs.set(iplists[i],data+"-end), ")
            server = smtplib.SMTP(mailfrom, 1025)
            print "opening connection to smtp server"
            server.set_debuglevel(True)  # show communication with the server
            try:
                server.sendmail(IPAddr, '172.16.10.98', data['body'])
                print "sending email..."
            finally:
                server.quit()
                '''
    return
#  def login(self,user,password):



if __name__ == '__main__':
    rs = redis.Redis(host='localhost', port=6379, db=0)
    rs.set('10.100.102.6',"")
    rs.set('10.100.102.8',"")
    rs.set('10.100.102.7',"")
    print "ok"
    x= rs.get('10.100.102.6')
    print x+"redis working"
#    imapObj=imaplib.IMAP4()
    server = CustomSMTPServer(('172.16.10.159', 1025), None)
    print "going to loop and run the server"
    asyncore.loop()
    rs.close()
