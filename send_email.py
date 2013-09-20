from fabric.api import *

import smtplib

def send_email(from, receiver, message):	
	try:
	   serveur = smtplib.SMTP('localhost')
	   serveur.sendmail(from, to, message)         
	   print "Successfully sent email"
	except SMTPException:
	   print "Error: unable to send email"