import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = ''
token = ''

def init(givenSender = None, givenToken = None):
	if not givenSender or not givenToken:
		print('Email Config Not Loaded\nOne or more arguements not supplied\nCheck nova-config')
	else:
		global sender 
		sender = givenSender
		global token 
		token = givenToken
		print('E-Mail Config Loaded')

def send_email(to, subject, message):
	global sender
	global token
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(sender, token)
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = "nova-bot@py"
	msg['To'] = to
	server.send_message(msg)
	server.quit()



