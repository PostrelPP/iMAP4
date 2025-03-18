import imaplib
import email
import logging
from email.header import decode_header
import os
import time

IMAP_SR = 'imap.gmail.com'
MAIL_LOG = 'prtestimap@gmail.com'
PASS = 'owzp uqhl jpsm oohc'
FL_TS = 'work_pr_imap/OLD-RED'
TIME_CHECK = 60

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def log_to_mail():
	mail = imaplib.IMAP4_SSL(IMAP_SR)
	try:
		mail.login(MAIL_LOG, PASS)
		return mail
	except imaplib.IMAP4.error as e:
		logging.error(f"Log failed: {e}")
		return None

def create_folder(mail, folder_name):
	status, folders = mail.list()
	if status != 'OK':
		logging.info("Failed to retrieve folder list.")
		return False

	if f'"{folder_name}"' not in str(folders):
		status, response = mail.create(folder_name)
		if status == 'OK':
			logging.info(f"Folder '{folder_name}' created successfully.")
			return True
		else:
			logging.info(f"Failed to create folder.")
			return False
	return True

def sort_mails(mail):
	mail.select('inbox')
	status, messages = mail.search(None, 'SUBJECT "[RED]"')
	if status !='OK':
		return []

	email_ids = messages[0].split()
	return email_ids

def process_emails(mail, email_ids):
	for email_id in email_ids:
		status, msg_data = mail.fetch(email_id, '(RFC822)')
		if status != 'OK':
			continue

		msg = email.message_from_bytes(msg_data[0][1])

		subject = decode_header(msg['subject'])[0][0]
		if isinstance(subject, bytes):
			subject = subject,decode()

		subject_clean = "".join(c if c.isalnum() else "_" for c in subject)
		email_folder = os.path.join(FL_TS, f"{subject_clean}_{email_id.decode()}")
		if os.path.exists(email_folder):
			continue

		os.makedirs(email_folder, exist_ok = True)

		text_content = ""
		if msg.is_multipart():
			for part in msg.walk():
				content_type = part.get_content_type()
				if content_type == "text/plain":
					text_content += part.get_payload(decode = True).decode()
		else:
			text_content = msg.get_payload(decode = True).decode()

		with open(os.path.join(email_folder, 'message.txt'), 'w', encoding = 'utf-8') as f:
			f.write(text_content)
		logging.info(f"Added message content to {email_folder}")

		attachments_folder = os.path.join(email_folder, 'ZALACZNIKI')
		has_attachments = False

		for part in msg.walk():
			if part.get_content_maintype() == 'multipart' or not part.get('Content-Disposition'):
				continue

			filename = part.get_filename()
			if filename:
				if not has_attachments:
					os.makedirs(attachments_folder, exist_ok = True)
					has_attachments = True

			filepath = os.path.join(attachments_folder, filename)
			with open(filepath, 'wb') as f:
				f.write(part.get_payload(decode = True))
			logging.info(f"Added attachment {filename}")

		mail.copy(email_id, 'OLD-RED')
		logging.info(f"Email {email_id} copied to OLD-RED folder")

def main_loop():
	while True:
		try:
			mail = log_to_mail()
			if mail and create_folder(mail, 'OLD-RED'):
				email_ids = sort_mails(mail)
				if email_ids:
					process_emails(mail, email_ids)
				mail.logout()
				logging.info(f"Refresh after {TIME_CHECK}")
			time.sleep(TIME_CHECK)
		except Exception as e:
			logging.error(f"Error: {e}")
			time.sleep(TIME_CHECK)

if __name__ == '__main__':
	os.makedirs(FL_TS, exist_ok = True)
	main_loop()
