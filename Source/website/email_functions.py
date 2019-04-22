import requests
import copy





class Email_functions:
	"""
	Available public functions:
	ticket_creation_new_ticket() - Called when nonadmin creates new ticket
	ticket_creation_nonadmin_replies() - Called when nonadmin replies to ticket
	ticket_creation_admin_replies() - Called when admin replies to ticket
	login_forget_password() - Called when password is forgotted

	"""


	email_sending_success = "Email is sent successfully"
	email_sending_error = "Error faced when sending email"


	def acnapi_email(self, email_recipient, email_subject, email_html):
		"""
		Private method, sends email to destination through support@accenture.com
		"""
		url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
		payload = {"subject":None, "sender":"support@accenture.com", "recipient":None, "html":None}
		headers = {"Host":"ug-api.acnapiv3.io", "Server-Token":None, "Content-Type":"application/json", "cache-control":"no-cache", "Postman-Token":None}
		token_file_contents = None
		counter0 = 2  # a counter that counts the number of values we need to retrieve from tokens.txt

		with open("tokens.txt") as token_file:
			token_file_contents = copy.deepcopy(token_file.readlines())

		for i in token_file_contents:
			if "Server-Token" in i:
				headers["Server-Token"] = i.split(":")[1][:-1]  # slice the string to remove "/n" char
				counter0 -= 1
			elif "Postman-Token" in i:
				headers["Postman-Token"] = i.split(":")[1][:-1]  # slice the string to remove "/n char"
				counter0 -= 1

		# check if all necessary values are retrieved
		if counter0 != 0:
			print("tokens.txt do not have the values acnapi_email() is looking for")
			return

		payload["subject"] = email_subject
		payload["recipient"] = email_recipient
		payload["html"] = email_html

		response = requests.post(url, json=payload, headers=headers)

		if response.status_code == 200:
			return self.email_sending_success
		else:
			return self.email_sending_error


	def retrieve_all_admin_email(self):
		"""
		Private method, returns dictionary of admin username (as key) and admin email (as value)

		Uses the inherent attribute "is_staff" of the createuser_extended_user mysql table
		"""
		output = {}
		all_admin = Extended_User.object.filter(is_staff=1)

		for admin in all_admin:
			output[admin.username] = admin.email

		return output


	def ticket_creation_new_ticket(self, nonadmin_username, nonadmin_email, admin_dict, ticket_title, ticket_id):
		"""
		Public method. Called when a new ticket is created by nonadmin. Emails nonadmin that new ticket has been created, and all admin to notify

		admin_dict is a dictionary that contains admin id (as key) and [admin username, admin email] (as value)
		"""

		if nonadmin_username!=None and nonadmin_email!=None:
			# for non-admin
			subject = 'Your ticket has been created'
			message = "<h3>{0}, your ticket is awaiting admin help</h3>".format(nonadmin_username)  # for dat personalization ;))))
			if self.acnapi_email(nonadmin_email, subject, message) == self.email_sending_error:
				return self.email_sending_error

		# for all admin
		subject = 'New ticket incoming'
		for i in admin_dict.keys():
			message = "<h3>{0}, there is a new ticket {1}</h3>".format(admin_dict[i][0], ticket_id)  # for dat personalization ;))))
			if self.acnapi_email(admin_dict[i][1], subject, message) == self.email_sending_error:
				print("@@@@")
				print("admin email: {0}; subject: {1}; message: {2}".format(admin_dict[i][1], subject, message))
				return self.email_sending_error

		return self.email_sending_success


	def ticket_creation_nonadmin_replies(self, assigned_admin_username, assigned_admin_email, admin_dict, ticket_title, ticket_id):
		"""
		Public method. Called when nonadmin replies to existing ticket

		admin_dict is a dictionary that contains admin id (as key) and [admin username, admin email] (as value)
		"""

		subject = "A reply is received for ticket {0}".format(ticket_id)

		if assigned_admin_username!=None and assigned_admin_email!=None:
			# if an admin is assigned to the ticket
			message = "<h3>{0}, there is a new reply to ticket {1}</h3>".format(assigned_admin_username, ticket_id)
			if self.acnapi_email(assigned_admin_email, subject, message) == self.email_sending_error:
				return self.email_sending_error
		else:
			for i in admin_dict.keys():
				message = "<h3>{0}, there is a new reply to ticket {1}</h3>".format(admin_dict[i][0], ticket_id)  # for dat personalization ;))))
				if self.acnapi_email(admin_dict[i][1], subject, message) == self.email_sending_error:
					return self.email_sending_error

		return self.email_sending_success

	def ticket_creation_admin_replies(self, nonadmin_username, nonadmin_email, ticket_title, ticket_id):
		"""
		Public method. Called when admin replies to existing ticket. If nonadmin did not opt to be notified, no emails will be sent
		"""

		if nonadmin_username!=None and nonadmin_email!=None:
			subject = "A reply is received for ticket {0}".format(ticket_id)
			message = "<h3>{0}, there is a new reply to ticket {1}</h3>".format(nonadmin_username, ticket_id)
			if self.acnapi_email(nonadmin_email, subject, message) == self.email_sending_error:
				return self.email_sending_error

		return self.email_sending_success

	def login_forget_password(self):
		pass
