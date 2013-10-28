import smtplib

def send_email(sender, receiver, message):	
	try:
	   serveur = smtplib.SMTP('localhost')
	   serveur.sendmail(sender, receiver, message)         
	   print ("Successfully sent email")
	except SMTPException:
	   print ("Error: unable to send email")
